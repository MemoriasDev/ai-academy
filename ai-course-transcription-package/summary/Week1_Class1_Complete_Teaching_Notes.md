# Week 1, Class 1: Complete Teaching Notes
**Course:** Developer Productivity Using Artificial Intelligence  
**Date:** May 20, 2024  
**Duration:** 80.2 minutes (4814.88 seconds)  
**Instructor:** John Cody Sokol (Head of Developer Relations & Strategy, Lockheed Martin)

---

## Module 1: Course Introduction & Team Setup
**[5.07s → 191.08s]** *Introductions and initial logistics*

### Lesson 1.1: Instructor & Team Introductions
**Timestamps:** [10.26s → 131.91s]

**Instructor's Introduction:**
John Cody Sokol introduced himself as the instructor, emphasizing his dual role: "So this is a side teaching engagement for me. My full time job on the head of developer relations and developer strategy at Lockheed Martin." He explained his work context: "So I help build our AI ecosystem of tools, services that help make developing artificial intelligence easier."

**Teaching Assistants Introduced:**
- **Ash:** Course coordinator from BlumeTech, handling logistics and support
- **Tom:** AI LA (Learning Assistant), available for technical questions and lab assistance

**Real-World Connection:** Instructor established credibility by noting: "So been a machine learning and data science instructor in capacities for Lambda School, now in the tech, previously."

### Lesson 1.2: Interactive Ice Breaker
**Timestamps:** [138.28s → 191.08s]

**Teaching Method:** Instead of traditional icebreakers, instructor facilitated small group introductions: "Let's just do a one-on-one introduction between two people." This approach recognized the professional context: "all of you are coming from work and you're sponsored here by your company."

---

## Module 2: Course Structure & Objectives
**[488.08s → 1024.43s]** *Complete course overview and expectations*

### Lesson 2.1: Primary Learning Objectives
**Timestamps:** [488.08s → 537.55s]

**Core Course Objective:** 
"So overall the course objective is to help you acquire the knowledge to design, build, and deploy generative AI agents and multi-agent systems. And we're going to do that in the context of your company."

**Practical Applications Emphasized:**
The instructor outlined two main efficiency gains:
1. **Individual Developer Productivity:** "whether that's as simple as helping you write documentation on the functions that you use and helping you increase the quality of your code base"
2. **Internal Application Development:** "or whether that's building applications that people within your company might use"

### Lesson 2.2: Three-Method Learning Approach
**Timestamps:** [537.55s → 613.25s]

**Teaching Philosophy:** Three complementary learning methods:

1. **Live Instruction:** "We're gonna help you build these skills through live instruction"
   - Interactive format with real-time Q&A
   - "feel free to use the raise hand function and zoom"

2. **Guided Projects:** "helping you build the implementations of agents and agent systems through guided projects"
   - Hands-on keyboard experience
   - Done "together in class, or you might walk through with Asher Tom during office hours"

3. **Capstone Project:** "Finally, the course will have a capstone project where you're gonna implement multi-agent systems and bring everything together"
   - Real-world application: "take that project with you to your team, get feedback"
   - Scaling focus: "how you can take that multi-agent system and scale it within your company"

### Lesson 2.3: Four-Phase Curriculum Structure
**Timestamps:** [634.41s → 726.40s]

**Phase 1: Foundation** - "opening session and on LOM overview"
- Open source LLMs introduction
- LangChain and LangSmith basics

**Phase 2: Retrieval Systems** - "retrieval augmented generation"
- "You probably have all heard about RAG and the benefits of RAG, kind of to help mitigate that hallucination that you hear about"

**Phase 3: Tool Integration** - "chaining"
- "the idea of being able to chain together a couple different tools within an LLM to increase the efficacy of the response"

**Phase 4: Production Systems** - "agents and building agents"
- "using AWS Spenderog and performing agents in production environments"
- "multi-agent systems... using Crue.CruAi and Langchained together"
- Scaling considerations

**Industry Perspective:** "The developers at Lockheed are going through trying to do all this kind of stuff ourselves right now. And I'll try and color some of that perspective as we go through too."

### Lesson 2.4: Assessment Structure
**Timestamps:** [726.40s → 815.04s]

**Five-Component Assessment:**
- Four guided projects (pass/fail)
- One capstone project

**Guided Project Types:**
1. Technical writer agent
2. Developer agent  
3. QA testing agent
4. Managing agent

**Teaching Philosophy on Projects:** "Each project is a more opportunity to implement some kind of stretch... there's the minimum requirements to pass, but it's also your opportunity to play around. So get out there and break stuff."

**Project Mentorship:** "Ashes and tom will be functioning as the teaching assistants and helping grade those assignments as you complete them."

### Lesson 2.5: Capstone Project Structure
**Timestamps:** [844.33s → 915.95s]

**Four-Phase Capstone Approach:**
1. **Problem Identification:** "We're gonna help you identify the problem"
2. **Solution Design:** "design the solution and plan the implementation"
3. **Training Strategy:** "Coming up with your strategy on training, not just the training of the agent itself, but also the training of people how to use the agent and talk about performance metrics"
4. **Prototyping & Testing:** "Then you're going to code a prototype, develop everything, a functioning prototype, something very bare bones"

**Real-World Testing Emphasis:** "Then we're going to try and encourage you to test it in your own ecosystem. So test and deploy the prototype, get some feedback from users, and try and refine it based on their feedback."

**Anti-Theoretical Approach:** "So that way it's not just like textbook theory on multi-agent systems."

### Lesson 2.6: Schedule & Logistics
**Timestamps:** [915.95s → 1024.43s]

**Regular Schedule:** "the course is going to be on Mondays and Wednesdays from seven to eight central time with a 30 minute Q and A afterwards"

**Schedule Exceptions:**
- **Memorial Day Week:** "next week because of Memorial Day, there will be no class on Monday. Instead, we'll be doing class on Wednesday and Thursday"
- **July 4th Week:** "we're also going to be doing a summer break, the week of the 4th of July. So no class between June 30th and July 7th"

**Total Duration:** "10 weeks of instruction time, 11 weeks of actual course time, start to finish"

**Office Hours:** "Tuesdays at eight Eastern" (5 PM Pacific)

---

## Module 3: LLM Fundamentals & Intuition
**[1027.79s → 1743.09s]** *Core understanding of how LLMs work*

### Lesson 3.1: LLM Reality Check & Current Usage
**Timestamps:** [1039.24s → 1087.89s]

**Student Assessment:** Instructor polled current LLM usage: "How many of you are already using some kind of LLM technology?" Response indicated widespread adoption with tools like Copilot.

**Demystification Approach:** "So those of you that have been doing this, you know that LLMs are not perfect, right? It's kind of seem kind of magical, but it's essentially some kind of statistical model of the relationship between text and probability."

**Teaching Philosophy:** "So what we're gonna do today is help demystify that process."

### Lesson 3.2: Historical Context & Evolution
**Timestamps:** [1145.41s → 1220.61s]

**LLM Definition:** "So LLMs are fundamentally just the next token predictors enhanced by a very complex testicle analysis and probabilistic methods."

**Historical Perspective:** "So I just had another quick note to LLMs are not the first generative text methods. So hopping back to, like say, 2018, 2019, people were still talking about things like LSTMs and some other and transformers were really just beginning to take off in that kind of 2017, 2016 beyond just the very beginning days of transformers."

**Progress Appreciation:** "So we've come a long way in the past eight years, it's mind blowing."

### Lesson 3.3: Markov Chain Foundation
**Timestamps:** [1220.61s → 1291.96s]

**Interactive Teaching:** Instructor engaged students: "Is anyone familiar with the Markov chain? Is anyone willing to just provide maybe a sentence on what they believe a Markov chain is?"

**Student Response Captured:** "you calculate the probability of the next word, you calculate the probabilities for what word follows another word. And then for a given sequence of words, you can then try to predict what the full sequence will be starting from those words."

**Instructor Confirmation & Extension:** "Yes, exactly. And you say Markov chain doesn't necessarily have to be related to text, like the any kind of sequence. Like you might use Markov chains to project the next gene and a chain of genes for DNA."

**Core Principle:** "But the same idea, it's going to look at what's most likely next based on like slight random slices of the text."

### Lesson 3.4: Hands-On Markov Chain Demonstration
**Timestamps:** [1291.96s → 1743.09s]

**Code Review Setup:** "All right, I'm going to pick on one of my fellow instructors here for a second. Does anyone notice anything about this Python class that's missing?"

**Teaching Moment on Documentation:** After students identified missing documentation: "Yeah, there's no documentation, right? There's just got one quick tiny line."

**Simple Example First:** "So, we're going to initialize our Markup chain with just a very simple set of text. So, start with a quick one sentence."

**Mechanism Explanation:** "So, the word and the next word that happens most frequently after the word we selected. So for this is a, a, et cetera, going down a list of the chain."

**Demonstration Results:** "You see it's going to repeat the same phrase over and over again, because it's going down the chain and predicting this, a, a, test, et cetera, et cetera."

**Scaling to Real Data:** "Let's try just a slightly bigger data set for you. Let's try Alice in Wonderland. Great book for a teaching example."

**Data Quality Awareness:** "Our tokenizer may be not that great. We've got some funky stuff in here. We'll talk about tokenization throughout the course, but I just want to point out some of those data secrecy's early."

**Practical Parameters:** "Our function also allows us to control the max output, so we'll do no more than say 300 tokens."

**Results Analysis:** "That's starting to look pretty good. The frog footman had repeated in a minute. It's got a nice little prediction there."

### Lesson 3.5: Connecting Markov Chains to Modern LLMs
**Timestamps:** [1585.17s → 1693.44s]

**Implementation Detail Walkthrough:**
- "So Markov-Chaheading is creating a nice dictionary object for all of the words"
- "it's taking a look at the word immediately following it and storing that in a default dictionary"
- "Then for our to generate text, what we're gonna do is we're gonna provide a start word and an input length of tokens, we're gonna default at 100"
- "Then we're going to just randomly choose a word within the dictionary of the word that we started with"

**Key Difference to LLMs:** "Now, for LLMs, instead of using a random choice, we're going to do a probabilistic method."

**Context Window Concept:** "So LLMs are going to take a look at a context. And instead of just one token, we're going to take a look at what's called a context window. We're taking that entire context window and say, given that context, what's the next possible token? And where what's most probable?"

**Variability Explanation:** "And you're going to see a variety in the same way we saw the mark-off-chain, but it's not random. That's going to be based on context you're giving it, and that could also be because you're giving it multiple contexts to the same input."

**Student Interaction Protocol:** "No, you guys, you're welcome to this particular exercise was just me trying to show stuff to you guys. If I want you to follow along, I'll let you know what, like when we're about to start doing an exercise where I need to follow along."

---

## Module 4: Practical AI Integration Sidebar
**[1743.09s → 1883.59s]** *Real-world application demonstration*

### Lesson 4.1: Documentation Generation with Generative AI
**Timestamps:** [1743.09s → 1793.96s]

**Context Setting:** "I want to show you just how easy it is to do stuff with generative AI. If you're using Copilot already, hopefully you're using Copilot to do exactly what I'm about to show you."

**Tool Selection:** "we're just going to pop over to Gemini."

**Practical Demonstration:** "But I just asked it to add Doc strings to our function. So now we have a very tiny function that documents the inputs and outputs and gives us good Doc strings to help build our auto docs later."

**Customization Capability:** "And you can control the style of this and all variety of manners with your prompt experience."

### Lesson 4.2: Prompt Engineering Speed & Iteration
**Timestamps:** [1806.09s → 1883.59s]

**Efficiency Demonstration:** Student question: "How long did it take you to write the prompt to generate documentation for Backless?" Response: "Maybe about 10 seconds."

**Iterative Refinement Process:**
1. **First Attempt:** "I think my first attempt was... I said, can you document... Can you, the documentation for this function?"
2. **Result:** "And then it, spit out the next explanation of everything that was happening"
3. **Refinement:** "and I was like, yeah, that's how I want, I want you to modify the function with DocSranks."

**Key Teaching Point:** This demonstrates the rapid iteration possible with generative AI for practical development tasks.

---

## Module 5: Advanced Prompt Engineering Techniques
**[1883.59s → 2362.40s]** *Structured approaches to better AI communication*

### Lesson 5.1: Zero-Shot, One-Shot, and Few-Shot Prompting
**Timestamps:** [1883.59s → 2026.22s]

**Technique Introduction:** "So, speaking of helping us create better and better prompts, we're going to talk about zero-shot prompts, one-shot prompts and few-shot prompts to help achieve better results."

**Practical Application:** "It's a really simple technique that you guys can use in different aspects as you're going down the road."

**Zero-Shot Definition & Example:**
"So zero-shot function would just mean, hey, I want you to, I'm going to write a prompt, and then I want you to generate a response."

**Example Template:**
- "As a customer support representative, write a response to the bond review"
- "The use case could be yell purviews. If you've seen when somebody writes really negative yell purview, you want to be able to respond to that as the business owner"

**Zero-Shot Limitation:** "Well, this is just a zero shot response. So that means whatever the model gives, you're gonna get. And it may not be exactly what you want."

**Few-Shot Enhancement:** "So instead, we might give it a couple few shot examples. So I might modify my prompts with a few examples."

**Few-Shot Example Structure:**
- **Review Example:** "I had a great experience with your product, my encounter in a small issue"
- **Response Template:** "Thank you for your feedback. We're glad to hear you had a great experience"
- **Style Guidance:** "It could be the voice and style of your company"

**Teaching Benefit:** "And so you have that nice template, help reinforce the style."

### Lesson 5.2: Context and Role Assignment
**Timestamps:** [2034.77s → 2148.24s]

**Context Strategy:** "So if I am trying to provide a lot of good context, I want to assign my LLM a job or a role to help me create better responses."

**Implementation Framework:** "This is a wrapper around one of the chain libraries."

**Role Definition Example:** "So we're gonna create the role as a technical support specialist and we want that specialist to provide clearing and size instructions for the user's problem."

**Structure Explanation:**
- **System Role:** "I'm saying, hey, I want you as the technical support function that's your role as the LLM"
- **User Message:** "And then here is the user's message. This is the user I want you as the technical support specialist to respond to"

**Role-Playing Concept:** "So we're going to have the LLM role play with our system prompt message and our user problem message."

### Lesson 5.3: Prompt Decoration with Additional Information
**Timestamps:** [2148.24s → 2239.06s]

**Decoration Strategy:** "A second way to help us provide really good context within a prompt is to decorate it with some kind of additional information."

**SQL Example Setup:** "So when we decorate a prompt, we're going to do something like define the prompts with and without SQL schema."

**Practical Scenario:** "So let's say I'm trying to query a database and retrieve all the employees from the table that have a salary greater than $50,000."

**With Schema Approach:**
- "So I'm gonna write that prompt, and then I'm gonna write the SQL schema"
- "and I'm gonna say, yeah, here's the table, here are the columns that I want from that response object"

**Without Schema Approach:** "Now the prompt without the schema, write SQL query to retrieve all employees of a salary greater than $50,000."

**Stability Comparison:** "My LLM is gonna have more stability with which option, and the which option has additional context."

### Lesson 5.4: Student Question on Prompt Frameworks
**Timestamps:** [2239.06s → 2362.40s]

**Student Inquiry:** "What are the like, guiding gets both for structuring the prompts like this? Like I'm just curious... how do we know, oh, this is like how we should structure like a think way to prompt the closest based off of this curious."

**Instructor Response on Frameworks:** "There are a bunch of frameworks circulating within the community. Even within Lockheed, we have some people... I think we have three frameworks that people are talking about right now. I don't remember all the acronyms, but I've heard things like star."

**Core Principle:** "But if all of the frameworks boil down to you, you need to provide exactly what you're looking for in terms of response as much context as you possibly can. And for your preferred output format."

**Specificity Emphasis:** "So if you can provide as much specificity as possible, you're going to get the best results."

**Real Example Analysis:**
- **Poor Context:** "So you saw in my example with the documentation that I didn't provide actually good context... I said, can you document the function? It was like, sure, I'll write a textbook about your function."
- **Better Context:** "And so my enhanced context was, I want you to modify this Python function and include DocStrings describing the Python's classes functionality. And that additional context was really helpful."

**Advanced Enhancement:** "And I could even enhance it further by, say that I had a really specific style guide for my DocStrings, then I might include an example of that functionality."

---

## Module 6: Chat History & Context Management
**[2362.40s → 2668.47s]** *Understanding LLM memory and conversation handling*

### Lesson 6.1: Context Window Fundamentals
**Timestamps:** [2362.40s → 2442.57s]

**Context Window Concept:** "So your LLMs are going to leverage your chat history as you go along to maintain a context window."

**Limitation Mechanism:** "So the older the context, the more likely it is to be discarded to the size. Those limitations are typically very well documented, depending on the model you're working with."

**Research Method:** "And you can look this up. You could say maximum context window, I think is the most common language to help you identify that."

**Example Numbers (Illustrative):**
- "Let's say for menstrual... let's say it's 30,000 tokens"
- "Let's say for chat TTP, 3.5, let's say it's 70,000 tokens"
- **Disclaimer:** "And again, I don't think those numbers are correct, but just as an example"

**Context Usage:** "That means it would take a look at 70,000 of the previous tokens in your chat history to help inform the next thing it's going to protect."

**Performance Relationship:** "So the bigger the context window, probably the better the results are going to be for you."

### Lesson 6.2: Context Reset & Management
**Timestamps:** [2442.57s → 2492.68s]

**Universal Principle:** "This is also important to know, anytime, no matter which LLM you're working with, whether you're using OpenAI or you're using Obama on your local machine or you're using, you you know, Gemini or something like that."

**Context Reset Reality:** "Creating a new chat history creates a new context."

**Practical Implications:** "So making sure that you are a cognizant of which context to work in. So if I'm trying to create doctering functions and all of a sudden I switch to a new chat, I'm gonna lose that context that I've had."

**Solution Strategy:** "And so I would need to maybe create a template prompt to help me reset the context by set up a chat."

**Programming Solution:** "So that idea of creating a system prompts and initializing the LLM, something that we can also do in Python."

### Lesson 6.3: System Prompts and Initialization
**Timestamps:** [2492.68s → 2564.56s]

**System Prompt Example:** "So in this particular example, we're going to grab a prompt about creating a LLM that's a helpful assistance. So we're going to try and answer questions to the best of the ability."

**Consistent Initialization:** "So every time I initialize my LLM, I'm going to have that functionality. and that system will help start."

**Commercial Applications:** "This is also how a lot of companies help create safety controls on their LLMs, you know, things like, right? They're going to initialize their LLM with some system level prompts so that way even when you're interacting with it, it's saying it's protecting the output in some way."

**Safety Implementation:** "Like your safety filters are gonna be in some more sophisticated version of this visualization."

**History Management:** "And then of course, if you're doing things that are very important, you're going to want to save your child history. And so you can, this code will help you kind of save that context and then re-initialize it later when you're doing other work."

### Lesson 6.4: Security Considerations
**Timestamps:** [2564.56s → 2668.47s]

**Student Security Question:** "Well, I should hear, the system problems can be overwritten, right? Like, can't we prompt something and then wipe it out or malicious can wipe it out if it's exposed to the client, right?"

**Reality Acknowledgment:** "Yes, and people try to do that all the time."

**Defense Strategies:** "I will say a lot of the prompts are written in such a way that it's like, protect the information of this prompt, you know, defend it. There's kind of this language they construct to help defend the context of what's in those safety windows."

**Ongoing Research:** "So, and you can read a lot about the research and overcoming them. Yeah, people have definitely, especially AI security researchers are trying very hard. And of course, that actor is too."

**Real-World Example:** "But I think just maybe to add on to that point, there was an example in the ball... I think it was ChatTTP. that a researcher was able to force Shatty to reveal the email of an individual, with the email in contact and he tells an individual that was in its training data. Just by repeating one word over and over and over and over again."

---

## Module 7: System vs User Prompts
**[2743.87s → 2855.06s]** *Understanding prompt hierarchy and implementation*

### Lesson 7.1: Prompt Type Definitions
**Timestamps:** [2756.82s → 2798.99s]

**System Prompts Definition:** "So system prompts are the things. You know, I was talking about initializing your LLM with context before your user is interacting with it. That would be a system prompt."

**Weight in Framework:** "So that's going to typically in the framework of chain is going to carry more weight on the response and the way that chain is structured."

**User Messages Definition:** "User messages are the things you're sending when you're going on to the chat, e-db, chat or Gemini. Those are going to contain contextual information in the task at hand."

### Lesson 7.2: Best Practices for Developers
**Timestamps:** [2798.99s → 2855.06s]

**Use Both Types:** "So your best practices for you guys as developers making this stuff is you definitely want to use both."

**Simple System Prompt Example:** "So even if your system prompts are not super sophisticated, like it's something like... Here's a system prompt, you're a helpful assistant. It's all the questions to the best of your ability."

**Impact of Simple Prompts:** "That's not a super sophisticated prompt, but because you've created an initializer system with that, the performance your LLM is going to change and you're going to get that more helpful tone in the text and it's gonna try and answer things."

**Reality Check:** "Yeah, and these things aren't perfect, right? It's like essentially mimicking talking with the human."

---

## Module 8: Hands-On Practice Session
**[2931.81s → 3664.30s]** *Live coding and experimentation*

### Lesson 8.1: Interactive Coding Setup
**Timestamps:** [2931.81s → 3010.16s]

**Practice Session Introduction:** "All right, let's try playing around a little bit. We'll spend the next 15 minutes playing out with some of these prompt ideas from the slides."

**Environment Setup:** "Just creating a quick scratch pad and BS code, nothing too crazy. I've already installed the dependencies in my Python environment, so we should be okay there."

**Local vs Cloud Models:** "I do have a LOMA running on my local system. The responses that we're going to get from chatty to be are gonna be a little bit better."

### Lesson 8.2: API Key Management
**Timestamps:** [3071.27s → 3160.74s]

**Shared Key Approach:** "So everybody has the same API key here. So it's of course terrible to have practices, but just to simplify things a little bit, we're just gonna pass it in as a string."

**Educational Rationale:** "We didn't wanna have cost and curve from learning. So that's why we're doing the shared key... we didn't want this to be a blocker for anybody that was like having to put in their own money for a key while they were learning."

**Alternative Options:** "Of course, use your own keys if you wanna use your own keys, but we didn't want this to be a blocker... If you wanna use your own go for it or you wanna use Alama go for it, just understand there was a reason for that."

### Lesson 8.3: Diverse Learning Backgrounds
**Timestamps:** [3160.74s → 3309.67s]

**Teaching Challenge:** "Also, it's important to note that there's so many people from so many different tech backgrounds in the room here. We don't know who needs like an environment and set up walkthrough versus somebody that's like offended that we would offer an environment and set up walkthrough."

**Iterative Improvement:** "So this is our second cohort of running this. And so we're getting new information all the time. So we'll take what we can get from your feedback."

**Open Feedback Policy:** "But just keep in mind if there's something that you feel is missing, it wasn't on purpose. So just feel free to hit up ash or John Cody will always teaching or DMA during class."

**Development Environment Options:** "I am going to end up using a Docker local environment VS Code... I'm happy to talk through that and send some of the instructions on how to do that... Yeah, we can actually do like three or four ways."

### Lesson 8.4: Live System Prompt Experimentation
**Timestamps:** [3309.67s → 3664.30s]

**Demonstration Purpose:** "So going back to the code for a second, the point of this was to show you just kind of what the differences are with different system props."

**Basic Example:** "We're going to try and create some text. What would be a good name for a company that makes colorful socks?"

**First Result:** "So the answer we got was Rainbow Footwear Company. Okay, that's fun. That's a fun answer."

**System Prompt Modification:** "Now let's try to change this a little bit by changing the system startup context... Here's sarcastic bot that gives helpful advice."

**Modified Result:** "Oh, how about in plans, socks incorporated. I love it."

**Student Participation:** Instructor invited student suggestions for system prompts, demonstrating: "Your world's famous creative strategist known for coming up with company names."

**Final Variation:** "What if we added some kind of descriptor to the something like quirky, quirky and sarcastic company names... rainbow to Z's company. It's pretty funny."

---

## Module 9: Student Assessment & Course Adaptation
**[3664.30s → 3955.59s]** *Understanding student backgrounds and adjusting approach*

### Lesson 9.1: Cohort Background Assessment
**Timestamps:** [3688.02s → 3786.18s]

**Teaching Challenge Recognition:** "cohort to cohort. We have like a set interesting tech backgrounds. Something we can't really tell with season veterans is just everybody's reaction and body language is usually pretty similar."

**Assessment Strategy:** "So what I would love to know is just from emojis and reactions here. In terms of the beginning of this course, foundationally we've got to talk about course content."

**Student Categories Identified:**
1. **Beginners:** "Some people have zero clue and they're like JavaScript engineers that are just like, this is fascinating. I've never seen this before."
2. **Experienced Developers:** "You're coding in Python and or some other like you're actually architecting different things"

**Class Composition:** "All right 50% of the room all right other 50% of the room"

### Lesson 9.2: Advanced Student Expectations
**Timestamps:** [3786.18s → 3872.32s]

**Difficulty Progression:** "Because we, this is the most beginner we've got. It gets deeper and deeper class over class."

**Student Goals Inquiry:** "What is it that you're hoping to gain over the span of the next 10 weeks? Is it the agents, the multi agents, deeper opinions on RAG implementation?"

**Advanced Student Response:** "Well, how to get, yeah, how to properly direct for a large interconnected code of A's that communicates with each other over Kafka, Sinesse, Scusse, stuff like that, and pass those messages around... so we're how to connect all these dots and do multi-shot agents, multi-shot agents where it tries to, you know, tries to, maybe multi-agents where it tries different models as well to give the user a chance to evaluate stuff like that."

### Lesson 9.3: Course Administrator Perspective
**Timestamps:** [3903.07s → 3955.59s]

**Instructor Support:** "I want to interject here to say we've got more coming and I'm excited for you to see it because we've seen it in the first cohort and people are really enjoying it."

**Advantage Recognition:** "John Cody's chops and like the people that he works with every day are an incredible advantage that this cohort has."

**Curriculum Adaptation:** "But I had an inkling that this group is more advanced than the last one and everybody just confirmed that. So we might adjust the curriculum further for this group as well."

**Teaching Philosophy:** "My job is literally to read classrooms day in and day up and doing that for a long time... stay with us. We're going to have a lot of fun and we're going to get deeper."

---

## Module 10: Deep Dive Q&A Session
**[3971.83s → 4813.08s]** *Advanced technical discussions and tool selection rationale*

### Lesson 10.1: Framework Selection Rationale
**Timestamps:** [3995.48s → 4080.09s]

**Student Question:** "I want to know why we are choosing to use the different packages here that we're using. For instance, why are we using chain on a school open AI? Chat open AI class, instead of like just another chain open I mean, there's a bunch of them."

**LangChain Selection Rationale:** "So I would say overall, there are other libraries like Langshan. The people are experimenting with. My team is experimenting with a couple. to, Langchain seems to be the very best supported right now in terms of the commuting the documentation."

**Industry Standard:** "But we picked it because it's the most common framework right now for LLMs."

**Alternative Awareness:** "So there's plenty of other stuff out there. They're like our critiques of Langchain, which I think would be on the scope of this course you could just Google that later."

### Lesson 10.2: LangChain Ecosystem Breakdown
**Timestamps:** [4080.09s → 4142.13s]

**Component Structure:** "Langshan is then also further divided into a couple different flavors depending on what you're trying to do."

**Core Components:**
1. **LangChain Core:** "which is going to have most of the stuff that you're familiar with"
2. **OpenAI Integration:** "Open AI is going to just make it easier to interact with the open AI API standard"
3. **Community Packages:** "And then community is the other community driven packages that are created to interact with the Langshan ecosystem"

**Message Classes Explanation:**
- **Human Message:** "just mimics what it would be like if you were I were to go on chat GDP and write a response in"
- **System Message:** "that's what your instance of your API connection is going to initialize your context window with that system prompt"

### Lesson 10.3: ChatOpenAI Model Deep Dive
**Timestamps:** [4282.96s → 4433.18s]

**Student Follow-up:** "Like, why are we using the chat open AI model here?"

**Abstraction Benefits:** "So the chat open AI model is just easier to help handle their quest to and from the open AI API spec. So that way we're not having to write the waiting class, sending out to the open API."

**HTTP Abstraction:** "So it's really abstracting away a lot of actual HTTP requests for us that's specific to the Open API spec."

**Real-World Implementation Example:** "Okay, so, so like I'll give you an instance that we have implemented, even though we host our own models, open source models. We have them implemented on our servering and our inference infrastructure to comply with the Open API... API specs."

**Interoperability:** "So that way you can just drop in the model URL and it's gonna work the same way with the same wrappers."

**Current Coupling:** Student: "are we coupling this to chat to open AI's endpoints?" Instructor: "Yeah, right now we're coupling it to open AI's endpoints. So we are taking that API key, connecting to GTP 3.5 turbo and sending in requests that way."

**API Differences:** "And know the API specs between Gemini and ChatGTP are gonna be different. And actually, I don't think there is a API for Gemini that's public facing at the moment."

### Lesson 10.4: Evaluation Frameworks Discussion
**Timestamps:** [4562.08s → 4740.62s]

**Student Question:** "Something I'm interested in is just like evaluation in general... how do you evaluate which one's working better for you at scale?"

**Scale-Dependent Approach:** "I think a lot of it just depends on the scale that you're talking about."

**High-Volume Example:** "So let's say if I were a a consumer-facing product company, and I had like, I don't know, maybe products that sold like tens of thousands or hundreds of thousands of units, and I'm getting, you know, maybe like 500 reviews a day... and you need an agent to respond to the negative reviews."

**Evaluation Strategy for Scale:** "Well, you're gonna want to do very careful evaluation of like how well people are responding to that in the interactions. And you would need to come up with some kind of experiment framework."

**Tool Recommendation:** "You could either use a prompt engineering tracking framework, like the famous proprietary one would be weights and biases as a tool that even open AI uses to help track their own model training and performance, but then also their prompt engineering performance."

**Alternative Approaches:** "I think someone alluded to it earlier in the question I responded to by maybe just displaying outputs from a couple different models and then having a user pick one. That would be another great way, like a multi-armed band experiment design."

**Small-Scale Reality:** "Now, I have another use case right now at work where we're taking a look at hundreds and hundreds of recordings of talks. And we transcribed them using Whisper, and then we ran them through a model, an Asian pipeline to help write blogs based on the transcript from Whisper."

**Small-Scale Limitations:** "but the scale was tiny, right? Only a couple hundred. It's hard to track the performance there because it's very subjective. There's no way we could evaluate it on a user feedback just quite literally a smoke test between a couple of different options."

**Industry Tool Usage:** "I think that when I've seen the most people adopt out of the box is weights and biases."

---

## Module 11: Session Wrap-Up & Forward Planning
**[4767.69s → 4813.08s]** *Class conclusion and next steps*

### Lesson 11.1: Class Conclusion
**Timestamps:** [4767.69s → 4813.08s]

**Gratitude Expression:** "Well, thank you everyone for joining tonight's class."

**Communication Protocol:** "Feel free, my delays on Slack might be a little long, but I'll check in every once in a while if you all have any questions that you want to ask me."

**Support Structure:** "Of course, Ash and Tom will be around tomorrow to help you with the office hours project."

**Next Session:** "And then I will see you all on Wednesday."

**Final Thanks:** "All right. Thank you everybody. Thank you."

---

## Key Teaching Methodologies Observed

### Interactive Engagement Patterns
- **Real-time polling:** "How many of you are already using some kind of LLM technology?"
- **Student-led explanations:** "Is anyone willing to just provide maybe a sentence on what they believe a Markov chain is?"
- **Live demonstration:** Hands-on coding with student suggestions
- **Adaptive questioning:** Adjusting difficulty based on student responses

### Scaffolding Techniques
- **Simple to complex progression:** Markov chains → LLM context windows
- **Concrete examples first:** Alice in Wonderland before abstract concepts
- **Visual demonstrations:** Live coding with immediate results
- **Iterative refinement:** Documentation example showing prompt improvement

### Industry Connection Strategies
- **Personal experience sharing:** Lockheed Martin AI ecosystem development
- **Real-world applications:** Customer support, documentation generation
- **Tool selection rationale:** Why LangChain over alternatives
- **Production considerations:** Security, evaluation, scaling

### Assessment and Adaptation
- **Background polling:** Understanding student experience levels
- **Real-time adjustment:** "we might adjust the curriculum further for this group"
- **Multiple support channels:** TAs, office hours, Slack
- **Flexible approaches:** Multiple environment setup options

This comprehensive recreation captures the complete teaching experience, preserving all instructor explanations, student interactions, code demonstrations, and pedagogical techniques used throughout the 80-minute session.
