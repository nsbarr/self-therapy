# dream_rag.py

import os
import logging
import time
from typing import List
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables and configure OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
client = OpenAI(api_key=OPENAI_API_KEY)

# Configure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "dream_dictionary.csv")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "embeddings")
EMBEDDINGS_PATH = os.path.join(EMBEDDINGS_DIR, "dream_embeddings.npy")

# Rate limiting settings
REQUESTS_PER_MINUTE = 150  # Conservative limit
SECONDS_PER_REQUEST = 60.0 / REQUESTS_PER_MINUTE
last_request_time = 0

# Create embeddings directory if it doesn't exist
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, model: str = "text-embedding-3-small") -> np.ndarray:
    """
    Get embedding for a text using OpenAI's API with rate limiting.
    
    Args:
        text (str): The text to embed
        model (str): The OpenAI embedding model to use
        
    Returns:
        np.ndarray: The embedding vector
    """
    global last_request_time
    
    # Rate limiting
    current_time = time.time()
    time_since_last_request = current_time - last_request_time
    if time_since_last_request < SECONDS_PER_REQUEST:
        sleep_time = SECONDS_PER_REQUEST - time_since_last_request
        time.sleep(sleep_time)
    
    try:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        last_request_time = time.time()
        return np.array(response.data[0].embedding)
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        raise

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors with numerical stability checks."""
    try:
        # Calculate norms
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        # Check for zero vectors
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        # Calculate dot product and similarity
        dot_product = np.dot(a, b)
        similarity = dot_product / (norm_a * norm_b)
        
        # Clip to valid range [-1, 1] to handle numerical instability
        return float(np.clip(similarity, -1.0, 1.0))
    except Exception as e:
        logger.error(f"Error calculating similarity: {str(e)}")
        return 0.0

def verify_files_exist():
    """Verify that required files exist and are accessible."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")
    
    logger.info("File verification complete")
    logger.info(f"CSV file found at: {CSV_PATH}")
    logger.info(f"Embeddings will be stored in: {EMBEDDINGS_DIR}")

def retrieve_similar_entries(
    query: str,
    top_k: int = 5,
    embeddings_path: str = EMBEDDINGS_PATH
) -> pd.DataFrame:
    """
    Retrieve similar entries for a given query.
    
    Args:
        query (str): The query text
        top_k (int): Number of results to return
        embeddings_path (str): Path to the embeddings file
        
    Returns:
        pd.DataFrame: Top k similar entries
    """
    df = pd.read_csv(CSV_PATH)
    if os.path.exists(embeddings_path):
        embeddings = np.load(embeddings_path, allow_pickle=True)
    else:
        logger.error(f"Embeddings file not found at {embeddings_path}")
        raise FileNotFoundError(f"Embeddings file not found at {embeddings_path}")
        
    query_emb = get_embedding(query)
    similarities = [cosine_similarity(query_emb, emb) for emb in embeddings]
    df["similarity"] = similarities
    return df.sort_values("similarity", ascending=False).head(top_k)

def batch_generate_embeddings(batch_size: int = 20) -> None:
    """
    Generate embeddings for all entries in the dream dictionary in batches.
    
    Args:
        batch_size (int): Number of entries to process in each batch
    """
    try:
        df = pd.read_csv(CSV_PATH)
        total_entries = len(df)
        total_batches = (total_entries + batch_size - 1) // batch_size
        
        logger.info(f"Starting embedding generation for {total_entries} entries")
        logger.info(f"Using batch size of {batch_size} with rate limit of {REQUESTS_PER_MINUTE} requests/minute")
        all_embeddings = []
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, total_entries)
            batch = df.iloc[start_idx:end_idx]
            
            logger.info(f"Processing batch {batch_num + 1}/{total_batches} (entries {start_idx + 1}-{end_idx})")
            
            # Generate embeddings for the batch
            batch_embeddings = []
            for idx, row in batch.iterrows():
                try:
                    embedding = get_embedding(row["full_definition_text"])
                    batch_embeddings.append(embedding)
                    logger.info(f"Processed entry {idx + 1}/{total_entries}: {row['term']}")
                except Exception as e:
                    logger.error(f"Error generating embedding for entry {row['term']}: {str(e)}")
                    # Use a zero vector as a placeholder for failed embeddings
                    batch_embeddings.append(np.zeros(1536))
            
            all_embeddings.extend(batch_embeddings)
            
            # Save checkpoint after each batch
            checkpoint_path = os.path.join(EMBEDDINGS_DIR, f"checkpoint_batch_{batch_num}.npy")
            np.save(checkpoint_path, np.array(all_embeddings))
            logger.info(f"Saved checkpoint for batch {batch_num + 1}")
        
        # Save final embeddings file
        np.save(EMBEDDINGS_PATH, np.array(all_embeddings))
        logger.info(f"Successfully generated and saved embeddings for {total_entries} entries")
        
        # Clean up checkpoint files
        for batch_num in range(total_batches):
            checkpoint_path = os.path.join(EMBEDDINGS_DIR, f"checkpoint_batch_{batch_num}.npy")
            if os.path.exists(checkpoint_path):
                os.remove(checkpoint_path)
        logger.info("Cleaned up checkpoint files")
        
    except Exception as e:
        logger.error(f"Error during embedding generation: {str(e)}")
        raise

def main():
    """Main function to test the setup."""
    try:
        verify_files_exist()
        logger.info("Testing OpenAI API connection...")
        # Test embedding with a small piece of text
        test_embedding = get_embedding("Test dream text")
        logger.info(f"Successfully generated test embedding with shape: {test_embedding.shape}")
        logger.info("Phase 1 setup completed successfully!")
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dream Dictionary RAG System")
    parser.add_argument("--generate-embeddings", action="store_true", help="Generate embeddings for all entries")
    parser.add_argument("--batch-size", type=int, default=20, help="Batch size for embedding generation")
    parser.add_argument("--query", type=str, help="Query to search for similar dreams")
    args = parser.parse_args()
    
    try:
        # First run the setup verification
        main()
        
        if args.generate_embeddings:
            logger.info("Starting embedding generation...")
            batch_generate_embeddings(args.batch_size)
        elif args.query:
            if os.path.exists(EMBEDDINGS_PATH):
                logger.info("Searching for similar dream interpretations...")
                top_matches = retrieve_similar_entries(args.query)
                print("\nTop matches for your query:")
                print(top_matches[["term", "full_definition_text", "similarity"]])
            else:
                logger.info("No embeddings file found. Please run with --generate-embeddings first.")
        else:
            logger.info("No action specified. Use --generate-embeddings to create embeddings or --query to search.")
            
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
