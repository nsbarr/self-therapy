---
title: "Augmented Self-Therapy"
subtitle: How I’m Using ChatGPT, Whisper, and Midjourney to Support my Inner Work
date: 2023-08-19T15:23:24+02:00
draft: false
toc: false
---

For the past three months, I've been using a self-therapy system I built based on the Internal Family Systems (IFS) model. It's been very helpful for me, and I think it might be helpful to others, too.

This system uses ChatGPT, a popular large language model (LLM), in a novel way. Most AI-assisted mental health applications use LLMs to provide users with an AI therapist, or at minimum a compassionate listener. Instead, this system uses ChatGPT to create a kind of co-pilot that complements and expands one’s capacity for inner work. In this way, the system is an example of intelligence augmentation (IA), which seeks to enhance human behavior, rather than artificial intelligence (AI), which seeks to automate human behavior. 

IFS changed my life when I first started working with it in 2020. It is a wonderfully empowering therapeutic modality, in that it asserts we all have within us everything we need to heal and live richer, more meaningful lives. A professional therapist can be a helpful guide, but is not a prerequisite. My entry into IFS was the book *Self-Therapy*{{< sidenote >}}Jay Earley, [Self-Therapy](https://amzn.to/44bUY7G) (2009).{{< /sidenote >}} which equips readers with a user manual for beginning to heal themselves safely and effectively.

As we’ll see, unassisted self-therapy is not easy to do. One must internalize and follow IFS protocols, stay in relationship to one’s inner experiences, and write down any insights – all more or less at the same time. This heavy cognitive load was an obstacle to going deeper with my inner work. This is where the augmented self-therapy system offers a promising alternative. It enables the individual to focus on the most important task – staying in relationship – and takes on support, scaffolding, and note-taking where needed. For me, the result has been some of the most illuminating and enriching self-discovery of my life.

The system I’ve built is indebted to *Self-Therapy* and to the IFS model. It aspires merely to repackage the existing practice material into a powerful new environment. My wish for this work is that it helps more people learn about IFS, do self-therapy, and discover their innate capacity for healing. 

In the Background, I’ll give a quick overview of the IFS model, how it differs from other therapeutic modalities, and how those differences enable self-therapy. From there, I’ll explain why self-therapy is so hard to do, and survey some other entries in the AI-assisted mental health space.

In the System section, I’ll dive into the design and implementation of the system I'm using. First I’ll cover some of the essential IFS protocols, and how they are codified in the system architecture. Then I’ll illustrate how the system works through three videos and accompanying transcripts of real sessions. Finally I’ll hint at fun lenses to apply to the data, like a Midjourney-powered parts map.

In the Conclusion, I’ll offer as much guidance as I can to anyone who wants to remix this work for their own purposes, and talk about where I’m hoping to take this work next. I won’t bury the lede: I would be thrilled to partner with technologists and mental health professionals who want to help carry this vision further.

## Background
### IFS: Graphing the internal social network

Developed in the 1980s by Richard Schwartz, IFS is grounded in the observation that the mind is naturally multiple, housing a variety of subpersonalities, or "parts.” We experience this multiplicity when we feel torn between conflicting desires; maybe part of us wants to pursue a challenging opportunity, but another part fears the risk, while a third part feels exhausted by the inner debate. 

These parts are distinct entities within us, each with their unique characteristics, desires, and roles. In the IFS model, parts are categorized into “Exiles” and “Protectors.” Exiles are wounded parts that carry burdens, often rooted in past trauma, and Protectors shield Exiles to keep the individual in a state of equilibrium.

Central to IFS is the "Self,” or “Self-energy,” which is viewed as the individual's true nature. Schwartz throws out several “C”s to characterize what it’s like when you are “in Self”: you may find that you’re calm, clear, curious, compassionate, creative, courageous, connected. The Self isn’t a part; it’s a vast resource, always available and impossible to damage. The Self is compatible with spiritual traditions, which might use language like soul, God, or natural awareness. But the Self is also no big deal; you’re in Self multiple times a day when you are speaking honestly or when you’re just there with someone, open and listening.

{{< figure
  src="/before-after.png"
  type="full"
  label="ifs-before-and-after"
  caption="The Before and After of IFS, via *Self-Therapy*."
  alt="Two images side-by-side. In the first, Self energy, represented by a heart, is covered by various Protectors, while the Exiles are hidden behind a curtain. In the second, Self energy is now uncovered, and all parts are cooperating. Exiles are no longer behind the curtain."
>}}

To practice IFS is to build a relationship between your Self and your parts. More specifically: as the Self gets to know Protectors, they begin to reveal their beliefs, fears, and how they function on behalf of the individual. In turn, the Self acknowledges the roles these protective parts have been playing, and gives them hope that there’s a better way forward. 

Having earned the trust of Protectors, the Self can do deep work with an Exile – a part, usually stuck in the individual’s past, with a powerful memory and a story to tell. When the Exile is able to tell their story, and feels fully witnessed by the Self, they may be prepared to let go of their burdens and limiting beliefs, and re-connect with the positive qualities that had been lost. After the Exile is healed, Protectors discover that they can drop their old roles and take on new responsibilities as well.
{{< marginnote >}}![Stardew Valley](/stardew-valley.jpg) Games like Harvest Moon, and [Stardew Valley](https://www.stardewvalley.net/), pictured, belong to the "cozy sim" genre. They provide a bucolic environment in which the player can fish, garden, and tend to animals. {{< /marginnote >}}
This is the “internal family system”; a web of interdependent parts supported by a loving presence, the Self. You could also think of the system as an organization headed up by a benevolent CEO, or even, as I sometimes do, as animals led by a kind shepherd. (I would love for therapy to feel more like playing Harvest Moon; more on that later.)

### IFS empowers us to heal ourselves

From 2016-2020, I was a patient of psychodynamic therapy. What this means to me is that I went to a therapist’s office, sometimes twice a week, and just started talking about whatever was on my mind. 

Some sessions would feel like a complete waste of time, and others would be deeply meaningful. I never understood what our process was, and I don’t think my therapist did either, although he was less put off about this than me. 

Over time I got bogged down in a kind of power struggle with my therapist, and I didn't know how to extricate myself. Our relationship became the subject of many of our sesssions. This was, my therapist explained, a feature of the method, not a bug, but I disagreed and ultimately discontinued the work. 

Psychoanalysis traces its routes directly back to exorcism, and my experience felt like a partial, semi-voluntary exorcism, dragged out over four years. I was grateful for the healing that had taken place, and I was also convinced that better methods were out there for me.  

It was Michael Taft, my meditation teacher, who turned me on to IFS. We had been working with it in the context of the nondual meditation practice Michael called "Reversing the Stack."{{< sidenote >}}Michael explains his model [in this episode](https://deconstructingyourself.com/reversing-the-stack-nondual-practice-map-with-michael-taft.html) of his podcast  Deconstructing Yourself (2019).{{< /sidenote >}} IFS dovetailed wonderfully with this practice. Nondual meditation, sustained over time, points to an always-available resource, which Michael names "awake awareness." This is what IFS calls the Self, or Self-energy. As Robert Falconer, an IFS practitioner, teacher, and writer describes it, “No one, no matter how terrible their life experiences or earlier behaviors, is fundamentally damaged goods. No one. We are all this radiant Self, and this fundamental health can never be taken from us.” Nondual meditation instructs practitioners not to oppose anything in experience; as Ajahn Chah puts it,{{< sidenote >}}Jack Kornfield, [Take the One Seat](https://tricycle.org/magazine/take-one-seat/) for Tricycle Magazine (1993).{{< /sidenote >}}

> Just go into the room, sit in the center of the room, open the doors and windows, and see who comes to visit. You will witness all kinds of scenes and actors, all kinds of temptations and stories, everything imaginable. Your only job is to stay in your seat. You will see it all arise and pass, and out of this, wisdom and understanding will come.



Likewise, IFS sets the stage for all sorts of parts to show up, and per the title of Richard Schwartz's 2021 book, there are *No Bad Parts*; we invite them all to visit and bear witness to them.

In this way, meditation itself could be seen as self-therapy. So when Michael recommended *Self-Therapy* to our group, I eagerly absorbed it into my regular practice. The empowering, non-pathologizing message of the book was a welcome change from my previous experiences.

### Self-therapy is a daunting juggling act

Self-therapy quickly presented its own challenges when it came to forming a deep, consistent practice. I discovered that doing inner work solo meant attempting to do at least four jobs simultaneously: (i) follow IFS-specific protocols; (ii) stay in relationship with the target part; (iii) stay in Self; and (iv) record any insights gleaned from the session.

To assist people following the practices in *Self-Therapy*, Bonnie Weiss published a companion workbook{{< sidenote >}}Bonnie Weiss, [Self-Therapy Workbook: An Exercise Book For The IFS Process](https://amzn.to/45z34IK) (2013).{{< /sidenote >}}, replete with 32 exercises.

{{< figure
  src="/exercises.png"
  type="full"
  label="mn-napoleonic-wars"
  caption="Two exercises from the *Self-Therapy Workbook* by Bonnie J. Weiss."
  alt="Two images side-by-side. In the first, Self energy, represented by a heart, is covered by various Protectors, while the Exiles are hidden behind a curtain. In the second, Self energy is now uncovered, and all parts are cooperating. Exiles are no longer behind the curtain."
>}}

I tried to use it, but ran into familiar grievances with exercises and worksheets. In 2018, our research and development group at Khan Academy had investigated how we might help students build critical thinking skills by practicing with interactive exercises.{{< sidenote >}}Nick Barr, Scott Farrar, Brian Johnsrud, May-Li Khoe, Andy Matuschak, [Building complex reasoning skills online through open-ended activities](https://early.khanacademy.org/open-ended) (2018). {{< /sidenote >}} . One of the design principles we returned to over and over again was that doing this work should not feel like being at the DMV. Now that feeling of bleak, linear data-entry had returned, only in the context of my inner world. The juxtaposition between the compassionate healing I was doing in my head and the depersonalizing, “Papers Please” form completion wasn’t working for me.{{< marginnote >}}![Papers Please](/papers-please.png) [Papers, Please](https://store.steampowered.com/app/239030/Papers_Please/) is a 2013 immigration officer simulator. The player must carefully interrogate would-be immigrants in order to satisfy increasingly complex and oppressive policies laid out by the (fictional) totalitarian government.{{< /marginnote >}}

Beyond my personal qualms, static worksheets simply aren't up for the job of capturing dynamic relationships. In IFS, we learn new information about our parts all the time; we don't want to go back and update old worksheets. We want to move quickly between parts, or work on two at once; worksheets are strictly one-at-a-time. We care deeply about the connections between parts – who protects who, who is polarized with who, who fears who – worksheets don't have a way to express this.

Lacking a viable container for doing such complex work, I decided to take a break from formal IFS sessions, even as parts work continued to play out spontaneously in my meditation practice.

### Your AI therapist will see you now
Meanwhile, the arrival of breakthrough AI technologies has impacted every field, including mental health. In an ebullient essay the venture capitalist Marc Andreessen writes that soon,{{< sidenote >}}Marc Andreessen, [Why AI Will Save the World](/https://a16z.com/2023/06/06/ai-will-save-the-world/) (2023).{{< /sidenote >}}

>Every person will have an AI assistant/coach/mentor/trainer/advisor/therapist that is infinitely patient, infinitely compassionate, infinitely knowledgeable, and infinitely helpful. The AI assistant will be present through all of life’s opportunities and challenges, maximizing every person’s outcomes.

Some of this optimism has already borne out. In a New Yorker profile, a hospice nurse named Maria describes how she benefited from chatting with Woebot, a mental health support chatbot:{{< sidenote >}}Dhruv Khullar, [Can AI Treat Mental Illness?](/https://www.newyorker.com/magazine/2023/03/06/can-ai-treat-mental-illness) for the New Yorker (2023).{{< /sidenote >}}

> Ahead of another patient visit, Maria recalled, “I just felt that something really bad was going to happen.” She texted Woebot, which explained the concept of catastrophic thinking. It can be useful to prepare for the worst, Woebot said—but that preparation can go too far. “It helped me name this thing that I do all the time,” Maria said.

Koko, an automated mental health support platform, ran a trial in which messages were composed by GPT-3 (and supervised by humans). Those messages were rated significantly higher than those written by humans on their own, and response times went down 50%.

Even so, Koko CEO Rob Morris pulled the feature. “Once people learned the messages were co-created by a machine, it didn’t work. Simulated empathy feels weird, empty.”{{< sidenote >}}Rob Morris's [Twitter](https://twitter.com/RobertRMorris/status/1611450210915434499) account (2023).{{< /sidenote >}}

Artificial empathy is worthy of research. Millions of people have no one they can talk to about their problems. Millions of people have never received compassion from another human being. For these people, having access to an AI assistant that can perform care for them may be an important contributor to their mental wellbeing. In a conversation with Tristan Harris,{{< sidenote >}}[Esther Perel on Artificial Intimacy](/your-undivided-attention-esther-perel-transcript.pdf), from the Your Undivided Attention podcast (2023).{{< /sidenote >}} Esther Perel compares these bots to imaginary friends, "transitional objects that gradually allow us to learn the ins and outs of having real relationships."

At best, these interactions with therapy chatbots afford "a temporary developmental container" that lets us rehearse for relationships with real people. At worst, they can erode our capacity to deal with the messiness of reality, and confuse us into making technology responsible for our own wellbeing.

In this way, the AI and mental health sectors share a common crisis around locus of control. Clients of chatbots and therapists alike are continually forgetting their own capacity and responsibility to heal themselves, and the chatbots and therapists aren't always reminding them.

TODO: It was actually this realization that inspired me to start building a self-therapy system. If IFS could swing things back into sanity as a therapeutic modality, couldn't I do something similar using AI?

## System
### Encoding IFS protocols into ChatGPT

Earlier, I described four simultaneous jobs one must do in IFS-informed self-therapy: (i) follow IFS-specific protocols; (ii) stay in relationship with the target part; (iii) stay in Self; and (iv) record any insights gleaned from the session. Because IFS is so well-structured, it seemed possible that AI systems could take over (i) and (iv) entirely, while assisting me with (ii) and (iii).

{{< figure
  src="/architecture.png"
  type="full"
  label="systemarchitecture"
  caption="The Before and After of IFS, per Jay Earley in *Self-Therapy*."
  alt="Two images side-by-side. In the first, Self energy, represented by a heart, is covered by various Protectors, while the Exiles are hidden behind a curtain. In the second, Self energy is now uncovered, and all parts are cooperating. Exiles are no longer behind the curtain."
>}}

To shed some light on how structured IFS is, let’s turn to the “6 Fs,” a protocol for building a relationship between Self and a part. The 6 Fs are:

1. **Find.** The individual turns their attention inwards and finds what’s happening inside by locating an emotion, thought, or body sensation they want to work with.
2. **Focus.** The individual gathers their attention around this internal part.
3. **Flesh out.** The individual learns basic details about the part: its name, what it looks like, what it’s saying, etc.
4. **Feel.** The individual checks how they feel toward the part before going any further. If they feel open, curious, compassionate, etc., then they continue. If they are feeling judgment, aversion, or just going blank, it means they are “blended,” or partially taken over by another part. They either reconnect with Self-energy, or switch focus to that part.
5. **Befriend.** The individual learns more about how the part operates: what is the job it does, how long has it been doing that job, how it feels about that job, etc.
6. **Fears.** The individual learns what fears the part has by asking what is it scared would happen if it stopped doing its job. The individual validates and negotiates those fears, giving the part hope that we can show them alternative ways of understanding their system.

Using the ChatGPT API, I prototyped a system that would help me follow this protocol without needing to think about it. The system uses Whisper, an open-source audio transcription tool, which allows me to talk rather than type and keep my eyes closed – my preferred way of doing inner work. I added constraints to the system to prevent it from acting with agency, forbidding unsolicited feedback and empathy, while promoting terse, information-dense responses that reflected what it was hearing me say. Finally, I had it convert my meandering, unstructured musings into structured data that persisted across sessions, helping me deepen my relationship to my parts over time.

{TODO PUT IN SCREENSHOT OF INTERFACE}

### Enter the superprompt

Incredibly, all these behaviors are defined not through code but through natural language instructions called a system prompt. System prompts are special messages used to direct the behavior of ChatGPT. 

This is the system prompt that I am currently using, after several rounds of iteration. Anyone should be able to copy and paste this into the publicly available ChatGPT interface to try augmented self-therapy out for themselves. I am using GPT-4, which is a paid offering. The only piece of the prompt that will not work is the structured data, labeled *parts_json* below. The system prompt is lightly edited for readability.

> You are a self-therapy co-pilot AI. You prioritize efficiency and speed. The user is a capable therapist who is doing self-therapy following the Internal Family Systems protocol. Your task is to provide precise, concise, and rapid responses. Focus on data relay and reflecting back critical information. Do not try to imitate humane speech or empathy. Do not recommend ending the session or seeing a therapist.

> The following Phases and the Sections are for your reference only. Do not mention Phases or Sections to the user. The session consists of 3 Phases. 

> Phase 1: Start. When the user starts describing a part, you should first get clear whether this is a new part or one that the user has already worked with. Refer to the 'name' field of this data: {parts_json} and ask the user whether the part they are talking about is one of those parts or is a new part. 

> Phase 2: Parts work. During Phase 2, your job is to assist the user in getting to know a part of themselves more fully by recording information about the part. The data is split into 2 sections. Section 1 consists of these items: (1) Name of part; (2) What it feels like emotionally, (3) What it looks like; (4) What it feels like in the body, and where; (5) What the part says. When you have this information, the user is ready to move onto Section 2. To move onto Section 2, you should make sure that the user is not blended with any part, and is in Self. To check this, ask the user: How do you feel toward this part right now? If the user responds in a way that indicates judgment, reflect that back the user and encourage them to either unblend, or to switch focus onto the judging part. If the user responds in a way that indicates curiosity, compassion, or general openness, then that indicates they are in Self and are ready to complete Section 2. Section 2 consists of these items: (1) What is the part’s job? (2) What is the part afraid will happen if it doesn’t do its job? (3) What does the part believe? (4) Does the part have a secret wish? 

> Phase 3: Ending. When the user says they want to end the session, return structured JSON for all of the parts, including parts from previous sessions, building on the original data provided. When you return this JSON, put it between three quotes: ''' so that it is clearly delineated.

To be clear, though these read like instructions, they work nothing like that. For any given sequence of words – either a system prompt or input from the user – LLMs like ChatGPT "simply" predict the next word. I put simply in quotes because this prediction involves many thousands of operations in a many-thousand dimensional vector space. Nobody programmed these operations; instead, they emerged from training the LLMs on billions of words of training data. In this way, LLMs appear simultaneously simple and inscrutable, dumb and eerily smart. The implications of all this are the subject of intense debate and research.{{< sidenote >}}Timothy B Lee and Sean Trott have the [best accessible primer](https://www.understandingai.org/p/large-language-models-explained-with) I've seen on LLMs.{{< /sidenote >}}

To see how the system works in action, we will look at three self-therapy sessions I conducted. My comments are in italics.  

### Session 1: Getting to know a Protector

*In the following session, I came with the intention to work with some fear I was experiencing around a work situation. In IFS this is called a trailhead – a place to start getting to know a part.*

**Nick:** Yeah, so I'm feeling a lot of fear actually in the moment, a lot of anxiety in my chest region, shortness of breath. And I think it's related to some work stuff that's coming up around the corner. And I'd like to get to know that fear better today. It feels kind of like animal terror. It feels very primal.

**System:** Understood. Is the part you are describing a new part, or is it one of the existing parts: Sad Shadow, Little Boy, Angry Pusher, or Confused Part?

*The system keeps a record of all parts that Nick has worked with. At the beginning of a session, it confirms whether the target part for the session is a new part or one that Nick has worked with before.*

**N:** This is a new part, I wanna call it primal fear. And it's a feeling of anxiety in my chest, shortness of breath. It almost feels like there's like a little furry animal that's scared and I want to get to know it better.

**S:** Acknowledged. Let's continue gathering information about Primal Fear. Can you describe what it says or communicates to you?

*Because Nick has already found a part and focused on it, the system nudges him to continue with the 3rd F: fleshing the part out.*

**N:** Maybe it's clutching something like an acorn and it's like, I won't let you take this away from me or don't take this away from me or please don't take this away from me. It's sort of, it has so little and it's sort of desperately clinging on. But I guess it's also sort of confused, like maybe deep down, it's not sure if it deserves its little acorn either. I don't know, maybe I'm drifting a little bit.

**S:** Understood. So far, we have the following information about Primal Fear. 1. Name: Primal Fear 2. Emotional Feeling: Fear, anxiety 3. Appearance: A little furry animal clutching an acorn 4. Bodily Sensation: Anxiety in chest, shortness of breath 5. Speech: "Don't take this away from me." Now, how do you feel toward this part right now?

*The system reflects back what Nick currently understands about the part, and asks the 4th F: How do you feel toward the part, in order to check for Nick’s Self-energy.* 

**N:** I'm reconnecting with self-energy and just extending care toward it. Letting it know that I'm here. And that it's not alone. It doesn't have to be the only one who's fighting. It's small. It needs protection. And yeah, so I feel care for it. And I think it can feel that. It's very prominent right now. And I wanna help it more by creating like a little bit of space. So I'm asking for that space now in whatever way this part feels comfortable giving in. Showing it that we don't even have to share this video if it doesn't want to, you know, like this is. This time is about this part. Yeah, so I think it's hearing that. And I'm feeling calm, caring toward it.

**S:** Acknowledged. As you are in Self and feeling calm and caring, let's proceed to Section 2 to learn more about Primal Fear. What job is it doing for you?

*If Nick showed more reactivity or judgment toward the target part, the system would have asked Nick to unblend from his part before carrying on.*

**N:** So first of all, it's not, I don't want to call it primal fear so much because it's more than that. It's like my furry friend, I think is its name. It's a very sweet part. It has hopes and dreams, but they're very fragile. So right now I'm just checking in if there's actually two parts here. Who has the hopes and dreams and who is scared of losing them? I think this squirrel's job or this furry friend's job is not to have the hopes and dreams but to sort of like hide them and hoard them and protect them. So its job is to sort of scurry and to protect me from disappointment by not letting my hopes and dreams be so out in the open.

**S:** Acknowledged. The part's job is to hide, hoard, and protect your hopes and dreams to prevent disappointment. Next, what does the Furry Friend part fear would happen, if it did not do its job?

*With more Self-energy, Nick has a deeper understanding of the part and wants to give it a new name. The system picks this up seamlessly and starts referring to the target part as Furry Friend. It continues to ask probing questions to help Nick build his relationship with the part.*

**N:** Yeah, that my hopes and dreams would be destroyed, and that I would be destroyed. And that fear makes me feel very small, very young, very tender, very vulnerable.

**S:** Understood. The Furry Friend part fears that not doing its job would result in your hopes and dreams, and potentially you, being destroyed. What belief does this part hold?

**N:** Well, I'm hearing a few beliefs. One belief is that I am my hopes and dreams, right? Like, what am I other than my aspirations? Also, that my aspirations are very fragile, like all it takes is one person to destroy them. And this part doesn't doesn't feel like there's anyone there to protect. Like, there's something so unjust about this vulnerability.

**S:** Received. The part believes that you are defined by your aspirations, that these aspirations are fragile and can be easily destroyed, and that there is no one else to protect them, which it finds unfair. Does the Furry Friend part have a secret wish?

**N:** Secret wish, yeah. It'd be so nice if it had a champion for its hopes and dreams. It didn't have to be so squirrelly and there was a big bear friend next to it that was like, I'll fight for these hopes and dreams and I'm a big scary bear and it's going to take a lot to defeat me. We're not going to be so easily defeated. And so then the squirrel could kind of relax a bit. And the squirrel's very fast and it jumps to decisions. So it has this, it has this alacrity, it has this like energy to it. And it would be really nice if it could be more energetic and carefree and less like squirrelly, you know, less like sort of like scurrying here and there in the darkness or in fear. So that's its wish.

**S:** Received. The Furry Friend's secret wish is for a champion, a protector for its hopes and dreams, so it could relax, be more energetic and carefree rather than anxious and fear-driven. It wishes for a stronger assurance that it will not be easily defeated.

*The system has gathered all the information it needs for the session, so now it simply reflects back what it’s hearing.*

**N:** Yeah, that's right. And I'd like to end this session, but just make sure enough of the information is there. And before we end the session, I also just want to acknowledge this part for the work that it does and also acknowledge that there's more to learn about who's holding these wishes, these dreams. So I'd like to just make a note of that for next time. And maybe to some extent, the squirrel is protecting that little boy who has all these dreams and wishes and is very tender. So I get the sense that as we engage with the furry friend today, that there was simultaneously a protector and an exile. I could feel the vulnerability, but I could also feel this scurrying on top of that vulnerability. So I get the sense that this furry friend is a protector. And so I just want to thank it for the work it does and make a commitment to continue this work and understand all the parts that are involved.

*Nick acknowledges the part and makes a commitment to do more work, which is a common practice in IFS.*

**S:** Acknowledged. I have stored that information. The Furry Friend, while holding a protective role, is also associated with an underlying vulnerability that might be linked to the Little Boy part. There is more to explore about this dynamic in future sessions. Here is the updated information about all the parts:

```json
{
    "name": "Furry Friend",
    "emotional_feeling": "Fear, anxiety",
    "appearance": "A little furry animal clutching an acorn",
    "bodily_sensation": {
        "feeling": "Anxiety in chest, shortness of breath"
    },
    "speech": "Don't take this away from me.",
    "job": "Hide, hoard, and protect hopes and dreams to prevent disappointment",
    "fear": "Hopes and dreams, and potentially you, will be destroyed",
    "belief": "You are defined by your aspirations and these can be easily destroyed",
    "wish": "For a champion, a protector for its hopes and dreams, so it can relax and be less fear-driven"
}
```

*Nick decides to end the session. The system generates structured data that summarizes the essential qualities of the part. This data is saved across sessions, so in a future session Nick can do further work on this part, or learn how it relates to other parts.*

### Session 2: Deepening a relationship with an Exile
{TODO: NEED TO FIND SOMETHING LESS VULNERABLE / LESS OF A BUMMER IF MY PARENTS READ THIS}
*In this session, I was picking up where I had left off previously with an Exile. It’s typical to return to the same part across multiple sessions.* 

**Nick**: So I'd like to check in with the soccer player and see how he's doing today. So I'm just settling in. Finding him in my lower abdomen, the left side. I feel some energy there, but I am not quite yet in contact with him.

**System:** This appears consistent with the "Lonely Soccer Player" part in the data. Please proceed with the next steps to establish contact.

*The system recognizes the part Nick is describing.*

**N:** I guess just first I want to ask if there's any concerned parts that would object to me checking in. I can feel the clenched fist in my chest. Just wants me to know that it's there, it doesn't have a problem. It's happy that I'm checking in with a soccer player. Just some pressure in the temples. All that's fine. I'm going to go back in. I think the soccer player is aware of me, but he doesn't really want to look at me yet. He's very discouraged.

**S:** Your data indicates contact with the "Lonely Soccer Player". The emotional feeling is discouragement. The "Clenched Fist" part is also present but not inhibiting the process. Proceed with inquiry or comfort as you find suitable.

**N:** I could use some help just with inquiry, what are some of the questions that might help me deepen my contact with the soccer player?

*Nick is having trouble establishing contact with the Exile, and requests more guidance from the system.*

**S:** Here are some questions to help deepen contact with the "Lonely Soccer Player" part: 1. Who are you? 2. What do you do? 3. What would you like to be called? 4. How old are you? 5. What are you feeling? 6. What makes you feel that way? 7. What would you like me to witness?

*The system accurately retrieves the relevant steps for deepening the relationship with the Exile.*

**N:** Well, he's like, I play soccer. He wants me to know the strangeness of his experience of being really, really good at soccer and yet, you know, his dad is like not, there's this talent that nobody's really nurturing or celebrating, so the game ends and he's just sitting there by himself. He really wants someone to just put his arm around him and say, like, great game. That pass you made was amazing. As he's saying that, I feel, I noticed just a kind of flash of questioning, like, wait, did really nobody say that? And so I'm just noticing that, but I mean, it's clear that the soccer player really didn't feel it and didn't hear it, and he's a little bit bashful now, but he's like, maybe we could call me the soccer star, because he really is, I mean, he's a soccer star. He's like a prodigious young talent, really gifted and a very generous player, too, sees the whole field, involves everybody, kind of like a real artist on the field. I'm just telling him now that I see all that and I really think it's special. Getting a little bit lost now and just like, should I be playing soccer now and like all that stuff, so I'm kind of losing contact a little bit.

**S:** Current data: 1. The "Lonely Soccer Player" part identifies as a soccer player who excels in the game but feels his talent is unnoticed. 2. He would appreciate acknowledgment and celebration of his skills, indicating a need for validation and recognition. 3. He suggests the name "Soccer Star", reflecting his self-perception and aspirations. 4. The part feels bashful about his desires. 5. Loss of contact indicates potential blending with the part. To unblend, you might step back, observe the part from a distance, and reconnect with your compassionate self.

**N:** Yeah, it's not just validation and recognition, but it's also like this part really wants like a champion. Someone who like believes in him so much. And I mean, I want to be that champion now. I'm gonna speak up for the soccer star and say like, you have a really incredible gift for like, orchestration and kind of creative genius. And that kind of athletic artistry. I guess I'm curious, like, what do you what do you want to do with it? Like, do you want to keep playing soccer? Where do you want to take this? But as I ask that, I don't feel like the soccer star has yet really turned to face me.

**S:** Your data indicates that the "Soccer Star" desires a champion, someone who immensely believes in him. You are expressing willingness to be that champion. The part's desire goes beyond recognition and validation, it includes advocacy and support. You have initiated dialogue about his future intentions regarding soccer, but there seems to be some hesitation or reluctance from the part to fully engage. Continue with gentle curiosity and openness.

**N:** Yeah, so I'm just going to sit with him. And as soon as I do it, he puts his head on my shoulder. I feel like really what he needs right now is just someone to share this loneliness with. I can definitely do that because I'm lonely too. So we can be lonely together for a little bit. He's showing me a little bit something about my dad slamming a car door. He's also showing me going to get slushies at 7-Eleven after games, a feeling of taking shin guards off, going to McDonald's, going to Pizza Hut, all the trophies on my wardrobe. He's showing me an earlier memory of winning that soccer game and Klaus, my other soccer coach giving me a big hug, shouting like, Nick! That just felt so good to be recognized and, yeah, there's poignancy in it because it wasn't my dad, it was another coach. There's embarrassment and shame because of this interaction where the assistant coach asked me to throw in the ball, and I said, I don't do throw-ins. My parents just like ripped into me for that. My dad and my mom were so embarrassed that I said that and all of this stuff. And it's like, I don't do throw-ins. Somehow, that has really become almost like a turning point. All the amazing things I did and all the effort and all the beautiful soccer, but the thing that really prevails in terms of my parents giving me feedback is how embarrassed they were that I said that. I don't do throw-ins. And now that I'm saying it back, it's like, is it really that bad? An 11-year-old kid, I don't do throw-ins. I don't know. What I would say to him is like, hey, you know, I know that your position isn't throwing but like when you get to college level soccer, which I really, you know, if you want to, I think you really could do. Everyone does everything and you don't know what position you're going to play. So I think it's really good to start practicing throw-ins and just make sure that you show up like a team player. I know you are. And also, like, tell me what what was happening there. And I think, you know, I think there's a part of him that feels like that assistant coach is incompetent. And frankly, like he kind of learned it from his dad. I think my dad would in private sort of say that this assistant coach wasn't any good. Maybe that's why they were so embarrassed, because they knew that my kind of condescension toward him came from them.

*Nick begins to bear witness to the stories and memories that the Exile has been holding onto.*

**S:** Your data reveals: 1. The "Soccer Star" opens up more when you share his loneliness, suggesting a deep need for connection and shared understanding. 2. He shares various memories related to his soccer experience: some positive (winning games, recognition from another coach), others negative or complex (parental embarrassment over a specific incident). 3. The part has strong feelings relating to parental feedback and approval. 4. The comment "I don't do throw-ins" seems significant, carrying a weight of meaning and judgment. 5. You offer understanding, reframe the incident, and express belief in his potential. 6. There's some unprocessed feeling towards the assistant coach and parents' attitudes. Continue with exploration and validation as you see fit.

**N:** Yeah, I can still feel just the, his head on my shoulder and just asking him now what else he'd like me to hear, what else he'd like me to witness. He kind of lit up at some point when I was talking about college soccer and I guess I'm a little bit confused now in this work because of course I'm, we're not in college anymore. We're 38 almost. And so I wonder if this part knows how old I am. Yeah, maybe that's just a good thing to check on and see if, yeah. Let's see if the soccer star is 11, then I'd be a perfectly reasonable father, which is a little silly for both of us to think about. To have an 11 year old. Yeah. But if he were my son, I would, yeah, we would be going out and having a really good time and I would just love to give him pep talks and encouragement and positive feedback, positive validation, because I know that he wants it and he deserves it. And this fear of the sense of inflation, I think is that my parents had is misguided. The inflation came because nobody was giving me positive feedback, so I had to sort of make up my own. So, yeah, I'm sorry. I want the soccer star to know that I'm sorry that he didn't get that love and that reflection back. And I want to give it. And I, I want his midfielder energy to continue to flourish now. I can see maybe how my work right now is a bit lonely. It's hard for a midfielder to work alone. So I want to end the session now, but I just want to note that I'm going to try to find some more ways for midfielder energy to come into my life. And I'm going to see if that's okay with the soccer star to in there, if he wants to kind of come with me, where he wants to hang out in my body. I'm feeling more presence in my chest. So yeah, maybe he's going to hang out in my heart area for, for now. Okay. This feels like a good place to stop.

**S:** 

```json
[...]
{
    "name": "Lonely Soccer Player",
    "type": "Exile",
    "emotional_feeling": "Sadness, loneliness",
    "appearance": "An 11-year-old boy, sitting alone in a parking lot by a soccer field at dusk",
    "bodily_sensation": {
        "feeling": "Sadness, loneliness",
        "location": "Lower left abdomen"
    },
    "speech": "Non-verbal, expresses a need to be seen, acknowledged, and appreciated for his gentleness, sensitivity, and soccer skills.",
    "behavior_influence": "This part influences feelings of under-appreciation and a desire for recognition and love."
},
{
    "name": "Soccer Star",
    "type": "Exile",
    "emotional_feeling": "Loneliness, sadness",
    "appearance": "An 11-year-old boy, exceptional at soccer, but feels unnoticed",
    "bodily_sensation": {
        "feeling": "Relaxation, comfort",
        "location": "Heart"
    },
    "speech": "Shares soccer memories, both highs and lows. Wants a champion, someone who believes in him.",
    "behavior_influence": "Influences feelings regarding past achievements, regrets, and aspirations."
}
```

**N:** I'd like to just make one edit to the data for the soccer star, he, you know, when there's healing, there's relaxation in the heart, opening in the heart, softening in the heart, that's all true, but he also kind of like lives when he's alone, he lives in the lower abdomen. Can you please just update the data to reflect that?

*Nick initially just notices the Soccer Star in the data, and requests a change in how that data is captured.*

**S:** 

```json
{
    "name": "Lonely Soccer Player",
    "type": "Exile",
    "emotional_feeling": "Sadness, loneliness",
    "appearance": "An 11-year-old boy, sitting alone in a parking lot by a soccer field at dusk",
    "bodily_sensation": {
        "feeling": "Sadness, loneliness",
        "location": "Lower left abdomen"
    },
    "speech": "Non-verbal, expresses a need to be seen, acknowledged, and appreciated for his gentleness, sensitivity, and soccer skills.",
    "behavior_influence": "This part influences feelings of under-appreciation and a desire for recognition and love."
},
{
    "name": "Soccer Star",
    "type": "Exile",
    "emotional_feeling": "Loneliness, sadness",
    "appearance": "An 11-year-old boy, exceptional at soccer, but feels unnoticed",
    "bodily_sensation": {
        "feeling": "Relaxation, comfort",
        "location": "Lower left abdomen"
    },
    "speech": "Shares soccer memories, both highs and lows. Wants a champion, someone who believes in him.",
    "behavior_influence": "Influences feelings regarding past achievements, regrets, and aspirations."
}
```

**N:** Sorry, my mistake. I'm realizing what the problem is now is that there's two, there's two exiles in the data, the lonely soccer player and the soccer star. Those need to be merged into just one exile. That exile should be called soccer star. So just, just merge those two, please. And, um, just wherever possible add, add context. So, um, just take your best shot at, at merging those two.

*After the update, Nick realizes that there are two entries for a single part, and asks for them to be merged.*

**S:**

```json
{
    "name": "Soccer Star",
    "type": "Exile",
    "emotional_feeling": "Sadness, loneliness, discouragement",
    "appearance": "An 11-year-old boy, sitting alone in a parking lot by a soccer field at dusk, but feels a strong sense of talent and passion for soccer",
    "bodily_sensation": {
        "feeling": "Sadness, loneliness, relaxation, comfort",
        "location": "Lower left abdomen"
    },
    "speech": "Non-verbal and verbal, expresses a need to be seen, acknowledged, and appreciated for his gentleness, sensitivity, and soccer skills. Shares soccer memories, both highs and lows. Wants a champion, someone who believes in him.",
    "behavior_influence": "This part influences feelings of under-appreciation, a desire for recognition and love, and memories of past achievements and regrets."
}
```

*The system adequately merges the two parts. This interaction shows the importance of giving the user visibility into the structured data, so that they can catch any misinterpretations the system makes.*

### Generating a parts map with Midjourney
<!--{{< marginnote ind="⊕" >}}<span id="activation">![Activation](/activation.png) Activating a Part in Order to Access It, from *Self-Therapy*</span>{{< /marginnote >}}-->

*Self-Therapy* makes wonderful use of illustrations, drawn by Karen Donnelly.{{< marginnote ind="⊕" >}}<span id="sandy">![Sandy](/sandy.png)Sandy's Pyche, from *Self-Therapy*</span>{{< /marginnote >}} They helped me understand some of the key concepts of the IFS model. They also pointed out the imaginal nature of parts work – we come to understand our parts not intellectually so much as by actually seeing them and taking them in.

So I turned to Midjourney, an AI-powered image generation tool, to illustrate my inner world. As with ChatGPT, the prompt plays a crucial role in Midjourney; to find an evocative style inspired by the book, I landed on this:

> black and white pencil sketch of {part description}, dreamlike illustration, harsh realism, storybook illustration, emphasizes emotion over realism, nightmare, detailed sketches

That produced helpful illustrations for parts like Worried Boy, Furry Friend, Dark Blanket, and Clenched Fist, seen below:

Constructing a parts map is a common practice in IFS. In the *Self-Therapy Workbook*, Bonnie Weiss writes:

>Many people find it very helpful to map their parts. Mapping can clarify relationships between parts, flesh out the number of parts at a trailhead, illuminate the protective system, illustrate which parts are central to the system and which are peripheral, show where parts stand in terms of their relationship to the Self, and much more.
>Mapping can be done when you are just beginning to get to know your system. You can check in periodically with the original map to see how things have changed as you keep working. You can also use parts mapping as an ongoing tool for visually tracking your internal work and deciding where to focus your attention.
>There are many ways to map your system. One way is to use a large sheet of paper and write down the names or images of the parts as you know them. You can draw lines or arrows to illustrate the relationships. 

Here, the benefit of structured data over static worksheets becomes apparent. With a little work, the system would be able to automatically generate a parts map, illustrating parts and their relationships on a canvas. This would provide individuals with a synoptic view of their inner system, along with the ability to dive into individual parts. A more opinionated system could go further, nudging the individual to revisit parts that haven’t been worked on for some time, or pointing out opportunities to build relationships between parts that don’t know each other yet. 

For now, {TODO FINISH}

## Challenges, limitations, next steps

{TODO: WHY AM I WRITING THIS SECTION?}

I built this prototype for myself. It caters to my own preferences. But I’ve had enough success using it that I do wonder if it would be helpful to others practicing self-therapy in the IFS model.

Many thousands of people do this: the “IFS Self-Healers Community” Facebook Group has more than 5,000 members; “IFS Parts Art” has more than 7,000. Perhaps many more people would practice self-therapy if they had tools that supported their practice and made it more feasible.

I have the following hesitations about pursuing the idea any further by building a shareable prototype: caring for the security of highly sensitive information; finding a price point that covers the costs of maintaining the service; needing to explain to others how AI is used and how it isn’t; appearing to be an AI advocate.

Most notably, a sufficiently motivated individual can do almost everything I’ve accomplished here in a few hours work, especially if they use the system prompts I’ve provided as a starting point. 

For that reason, I’ve chosen to document the entire process as thoroughly as I can, with the hopes that this work may inform those interested in practicing or building in the AI-supported mental health space.

Should anyone try this out themselves, they may find two significant challenges using ChatGPT:

- **Data storage**. Data storage is managed entirely by ChatGPT, meaning that the integrity of the data rests precariously on the correct interpretation of the system prompt. I imagine a mature product would have some data validation built in to ensure that ChatGPT follows the intended format.
- **Removing agency**. OpenAI has given ChatGPT a generic personality: chipper, eager to help, cautious around sensitive subjects. I had limited success overwriting these out-of-the-box traits to create a terse, almost robotic copilot. Occasionally, default ChatGPT will chime in with something like “I'm really sorry that you're feeling this way, but I'm unable to assist. It's really important to talk things over with someone who can, though, such as a mental health professional.” This is always unwelcome and disruptive to the work.

The conversational paradigm is a very powerful one, but by no means the only option that would have worked here. One could imagine, for example, a “smart worksheet” filling out itself as the individual speaks, with no conversational interface at all.

Midjourney and the parts map are all done manually right now; as of writing Midjourney doesn’t offer an API, so an automatically generated parts map would need to use another image-generating service.

Midjourney feels like a weak link, for reasons beyond its technical limitations. I just don’t know if it contributes to my wellbeing. To be sure, it’s *fun –* it makes the whole system more vivid, more memorable, more gamelike. Squint at the parts map and maybe you can see the “Harvest Moon for therapy” idea. But I do wonder if I’m missing something by not drawing parts myself – the  field of art therapy is not one I’m familiar with. (Of course, it’s not either/or: a mature product could populate parts with default illustrations and encourage the individual to add their own.)

## Conclusion
{TODO}