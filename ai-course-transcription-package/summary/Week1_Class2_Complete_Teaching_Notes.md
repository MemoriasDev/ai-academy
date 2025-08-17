# Week 1, Class 2: Complete Teaching Notes
**Course:** Developer Productivity Using Artificial Intelligence  
**Date:** May 21, 2024  
**Duration:** 49.1 minutes (2943.87 seconds)  
**Format:** Office Hours - Take-Home Activity Implementation  
**Instructors:** Ash (Course Coordinator), Tom (AI Learning Assistant)

---

## Module 1: Office Hours Structure & Format
**[3.38s → 55.79s]** *Setting expectations for office hours sessions*

### Lesson 1.1: Office Hours Teaching Methodology
**Timestamps:** [3.38s → 43.46s]

**Format Explanation:**
Ash outlined the structured approach: "Here's how office hours works. In terms of how we do an office hours, we'll take the take home activity at the end of last lecture."

**Three-Part Structure:**
1. **Take-Home Activity Review:** "Yesterday we had a take home activity of creating an LLM that summarizes to maintain chat history. We're going to do that with you in the beginning of the session."
2. **Open Q&A:** "Then we open it up for any questions that you guys may have."
3. **Comprehensive Support:** "You guys can then ask any questions regarding the course itself, any technical questions you have about the code, or any questions in general about just the layout of anything that's happening."

**Time Management:** "And then usually it takes about 40 minutes to an hour. If we end early, we end early, if we go along, usually we end up averaging about an hour though."

---

## Module 2: Technical Implementation Setup
**[55.79s → 197.25s]** *Environment and tooling configuration*

### Lesson 2.1: Development Environment Choice
**Timestamps:** [58.35s → 93.02s]

**Platform Selection:** Tom explained the demonstration approach: "Yeah, so at the moment we're doing kind of a summary chatbot basically for this. I can share screen, right? Let's just put it in there. So I've prepped the code for what we've got today."

**Dual Environment Strategy:** "What I've done is I've opened it up into a colab, just for ease of explanation. We've still got it on the VS code as well, with all of it there. So whichever you like to see, eventually we can show that."

**Accessibility Consideration:** The instructor chose Google Colab for demonstration while maintaining VS Code as an alternative, ensuring students could follow regardless of their development environment preference.

### Lesson 2.2: Environment Setup Process
**Timestamps:** [93.02s → 143.24s]

**Virtual Environment Creation:** "So if your setting up your stuff are for the actual initial stuff, you'll kind of want to make your virtual environment first like it says in the readme and then do a pip install or requirements to the requirements file and that will grab all of the bits and pieces and the stuff to actually make this work."

**Import System Overview:** "Then you want to kind of look at the the import system. So we're actually importing OS so we can grab a key from the .emv."

**Development vs Production Practices:** "At this point I'm not doing that in the collab. I'm just kind of hard-coded in it. So it's probably not a good idea to do that in real world terms but I've just unmatched quickly. Get it shown."

### Lesson 2.3: OpenAI Library Integration
**Timestamps:** [143.24s → 197.25s]

**Library Progression:** "And again loading the load.emv from .emv to kind of load it in. And then we're importing OpenAI. Now obviously under real world circumstances later on you'd probably be using something like but right now we haven't actually introduced it, so we're pretending that doesn't exist right now."

**Direct API Approach:** "So we're going to import OpenAI, so we've got access to the OpenAI chat stuff and things like that."

**Environment Variable Management:** 
- "Then if you've got this inside a .emv file, then we'll be loading .emv"
- "and then you'll be basically pulling in the API key and building out the client"

**API Key Verification:** "For now, I'll just print the API key to make it, sort of like show that we've definitely got that set."

---

## Module 3: Core Function Development
**[197.25s → 587.89s]** *Building the fundamental response generation functionality*

### Lesson 3.1: Generate Response Function Architecture
**Timestamps:** [197.25s → 269.78s]

**Function Purpose:** "So the next thing is we need to work on a function to generate a response. So it's basically it's going to generate text response based on a given prompt and model."

**Parameter Design:**
- **Prompt Parameter:** "It's taking parameters of prompt, and that's going to be the input string for the AI model to process."
- **Engine Parameter:** "And parameter of engine, and the engine is basically just the model. So it's just another word for the model, it's the engine that we use. And that's going to be the identifier used to generate the response."

**Return Value:** "So now we want it to return a string, and the string needs to contain the processed output from the AI model."

### Lesson 3.2: Implementation Details
**Timestamps:** [239.50s → 322.61s]

**Function Signature:** "So we take a look at the implementation or possibly implementation of that. We define in the generate response, we're taking in a prompt and we're hard coding the engine to kind of be GPT-3 turbo for now, but you can override that when calling it."

**Default Parameter Strategy:** "So we're just kind of having a fail safe and a thing to go to."

**Documentation Practice:** "So we've got a dark string here that generates text response based on given prompt model, pretty much what I've just gone over, same sort of thing. It's just here for clarity and to help anyone who's building it or anyone who's actually trying to understand what it does at a quick glance."

**OpenAI API Call Structure:** "Here we're creating a response and we're actually using the OpenAI, using chat completions, and we're creating a new chat completion. Then we're basing the model on the engine that's been passed in or the model that's been passed in."

### Lesson 3.3: Message Structure Implementation
**Timestamps:** [283.78s → 309.25s]

**Message Format:** "We're starting our messages, messages being a list of all of the messages that are there. We're starting it with the role user, content of prompt."

**Variable Usage:** "Now prompt is a variable that's been passed in along with the engine. So this is part of the overall building blocks of it."

**Error Handling Introduction:** "So we have a tricatch block because this could generate an exception. So we want to kind of catch that exception if it happens just to clean the and gracefully move out of it."

### Lesson 3.4: API Parameters Configuration
**Timestamps:** [322.61s → 398.86s]

**Parameter Breakdown:** "So this thing here, the create, that takes in the model, it takes in the messages, but also wants to know how many of the maximum tokens that we want to use."

**Token Limit Setting:** "So we can kind of tweak that a little bit. 150 seems to work out as a general basis to start with."

**Response Count Control:** "The end is basically how many times do we want to kind of generate a response for whatever prompt we give it. So in this case, we're just sticking with one to keep it very simple. It's only going to have one response and not have multiples."

**Advanced Use Case:** "In certain circumstances, you might want to change the end to a multiple response and then have the user kind of decide on a weighted average of what sort of response they want to take."

**Stop Parameter:** "Stop that's basically if we don't get any response from the actual chat completion then it will just send us none. We can decide what we want to send back that could be stop there, stop that and all stuff. But for our purposes, none works perfectly fine."

**Temperature Setting:** "And then the temperature, we're keeping it a fair medium sort of temperature. We're not going too high but we don't want it to zero just yet because we want to get some sort of variance in a response time in a response."

### Lesson 3.5: Response Processing and Error Handling
**Timestamps:** [398.86s → 499.10s]

**Potential Problem Identification:** "So that's basically just the simple most basic sort of thing to gain us a response. Now we would possibly come up with a problem where there are no choices."

**Choice Validation Logic:** "So if it doesn't generate a response and we try to return the response and we won't have choices so we're going to get some errors. So what we need to do is make sure that this is give us a response and in doing so we just say if the choices exist inside the response then we're going to return a choice 0 which is the first choice in this case it's only got one anyway and then give us the message but gives the content of the message."

**Data Cleaning:** "what we're going to do is strip in all of the whites based on all the bits and pieces that could possibly be error and in the way of clarity."

**Unexpected Response Handling:** "If choice is does not exist in the response, we want to kind of just let it know, let us know that it's had an unexpected response format and then give us kind of what the response looks like. So maybe it might be a weird strange object returning in some way or something's gone strange with the network where it haven't connected or something."

**Exception Management:** "The other unhappy case we need to deal with is if there's an exception, I'm kind of left as a very, very generic exception at this point. Ideally, in more than MVP, you're going to reiterate, I believe, you want to be a bit more specific with exceptions, and you probably want to have more of them down here."

**Fallback Strategy:** "If all of this just falls out and we fall down here, we just return an empty string. So we don't, you know, we don't actually give the user nothing, even though it looks like nothing, it means it's not going to just error out and break everything."

### Lesson 3.6: Student Q&A on OpenAI Version
**Timestamps:** [515.10s → 575.93s]

**Version Compatibility Question:** Student inquiry: "I saw in the requirements that TXT, it's sent to 0.28 of the OpenAI Library. is that what we're going to use? But they choose the format in 1.0."

**Educational Approach Explanation:** "Yeah, I was going to say moving forward, we'll probably use newer stuff. This was just for this simple explanation and the other stuff. And especially, you'll definitely want newer stuff if you're using things like lang chain because it uses all the newer things."

**Future Evolution:** "So literally next week we'll be using newer versions. This is just for this specific demonstration and ideas. It was the easiest way to quickly get it up and running just without letting chain and just get it there."

**Learning Exercise Suggestion:** "Another interesting thing for you to take away is take the code and try and update it to a newer version open out. There's some interesting little changes you need to do and some refactoring. So it'll be a nice little project for you to take home and have a little play."

---

## Module 4: Text Summarization Function
**[587.89s → 726.83s]** *Creating utility function for content summarization*

### Lesson 4.1: Summarization Function Design
**Timestamps:** [587.89s → 625.71s]

**Function Purpose:** "The next freestanding function we've got here is create summarized text function. All this does very, very simplistic function. It summarizes provided text using the specified AI model. So super simple."

**Parameter Structure:**
- **Text Parameter:** "It takes in some text as a parameter of text and that's the text to be summarized."
- **Engine Parameter:** "It takes in a bit of a pattern coming on here, takes in the actual engine and that'll identify the actual Engine what we're going to use for the summarization"

**Return Value:** "and then what it returns is a simple summary of the input text In other words, it's kind of a sorted excerpt of that text. It'll be an interesting format as well"

### Lesson 4.2: Implementation Simplicity
**Timestamps:** [630.95s → 704.62s]

**Code Structure:** "So the summarized, as you can see, it's pretty much a couple of lines. We could have got with a one line and with this, to be honest. But just for clarity, we've put it into multiple lines."

**Function Definition:** "So we define a function called summarize text. It's a free standing function. It takes in the text and takes in a default engine of GPT 3.5 turbo."

**Override Capability:** "But if you actually call it with an secondary, so you put your text in and you put something here, it's fine. You can override it. So it's fully over at the bottom of that point."

**Prompt Construction:** "And if we move down here, the actual summary prompt that we're giving it is just summarize this conversation literally. And whatever the text is. That's how simple we're doing."

**Function Reuse:** "And so we're just generating the response, using our previously made function. So that previous functional pair. So we're passing it, the summary prompt, and also what engine we're using."

**Modular Design Principle:** "So literally it's kind of simply using this free standard function within this one, just for clarity and to break it down into more reusable chunks."

---

## Module 5: Complexity Assessment Function
**[729.60s → 1157.63s]** *Developing conversation complexity evaluation*

### Lesson 5.1: Complexity Assessment Concept
**Timestamps:** [729.60s → 787.62s]

**Function Introduction:** "So again, we're going to create another setup. We're going to create another free standing function. And it's going to assess the complexity of some data. It's a very simplistic complexity assessor."

**Extensibility Awareness:** "You can write so many different ones. You can write entire trees and stuff. But we haven't gotten to that content yet in the syllabus. So we're going to be only showing you kind of a general idea of what we have covered already. So we're not going way outside of the scope."

**Core Functionality:** "So this one's just going to assess the complexity the conversation history and return a complexity score."

**Parameter Design:**
- **History Parameter:** "So its parameters are it's going to grab the history, a list of strings representing the conversations history."
- **Engine Parameter:** "It's again we can see a pattern here the engine so it's going to take in the engine to identify what we're going to be used to assess the complexity."

**Return Value:** "Then it's going to just return a simple integer representing the complexity score of the conversation so it's fairly straightforward and hopefully understandable."

### Lesson 5.2: Implementation Strategy
**Timestamps:** [796.87s → 947.88s]

**Prompt Construction:** "So, a possible way of implementing this based upon this criteria would be first creating complexity prompt, so we'll say assess the complexity of this conversation."

**Data Preparation:** "And in this code, we just simply join the history together with spaces. So we're basically kind of making sure that all of the different bits all stuck together and then we expect to get a complexity score."

**Simple Request:** "So that's all we do. Okay, tell me what the complexity is."

**Response Processing:** "So the thing here is the history and everything, we're going to be using that prompt to initially start it, we're going to then generate a response, utilizing the complexity prompt and passing it the end."

**Expected Response Format:** "So we'll have some text with, okay, here's the complexity of this stuff. So we'll have a bunch of text here with some verbose information, some text, but somewhere along the line, it'll have a number or a couple of numbers somewhere to kind of explain, hey this is how complex it is, it might have a 50, it might have a 35, it might have a 1.2, it depends entirely how complex it believes it is."

**Number Extraction Logic:** "So that's the number what we're going to be using and to extract that number we can say okay as long as complex text was not blank, we can break up the complex text into a single word so we're using it as a corpus, so we're using that complex to test as our corpus then we're jumping over every single word in the reverse of those complexity words."

**Reverse Processing Rationale:** "So we're going to take the end area because if you think about it's going okay give me the complexity score so it'll be near the end hopefully when it's being generated. So at this point we're going to reverse sort of read through it and if any of those words are a digit so if they're numbers we want to return that word as an integer because that will be the complexity score based upon our prompt."

**Fallback Value:** "If we get to the end of this and we don't get a single complexity score, we've got a hard coded return of a complexity of 20. Now this is completely arbitrary, we could change this to tweak it now and then, but that's That's just what we decided to just put there for now."

### Lesson 5.3: Student Questions on Complexity Assessment
**Timestamps:** [960.76s → 1157.63s]

**Purpose Clarification Question:** Student: "What is the idea of using this integer as a complexity assessment? Is that just a right?"

**Practical Application Explanation:** "It's a simplest way of looking at it and being able to have a finite specific number to say, if we have something to a certain complexity, then we want to automatically summarize it. So we're giving it a general idea of if it's too complex, then we want to summarize it and turn it into a summary instead."

**Utility Function Purpose:** "So that's the main utility function for the success complex."

**Alternative Approach Question:** Student: "But we're converting the, we're assessing it based off whether it's a number. This is just a demonstration of hypothetical complexity."

**Token-Based Explanation:** "Because we need some sort of function. OK, imagine you have a billion items in your history and you're asked to talk about those like summarise them. You don't necessarily, you want to kind of go, well, can they fit within the numbers?"

**Practical Token Management:** "So, what we probably would do is work out, for example... So see how we've got a max tokens. So what you do is you kind of work out how many words that maybe that max tokens would be. And what we want to do is, if we're going to kind of get cut off at some point in those max tokens. If we don't want it to just be cut mid-sentence, for instance."

**Prevention Strategy:** "So what we want to do is we want to be able to go, okay, if you're too long and you won't be understandable as a whole explanation, summarize it. So we need some sort of numeric value to kind of say, okay, only summarize if it's too big."

**Direct Token Counting Question:** Student: "OK, but why don't we just count the tokens and the history? Or is that what we're trying to do?"

**Modular Design Reasoning:** "We're trying to try and do that, but in a deterministic way and a tooling-based way. So now, if we want to, we're just basically calling this. So what we can do is, without having to change a load of hard-coded stuff inside the main logic, we can just change something in here and change how it deals with complexity."

**Extensibility Benefits:** "This could even be hitting a different API and pulling some data from that to find out the complexity. So there's a lot of different things you can do with it. And it's more a way of modularizing the code."

**Alternative Implementation:** "Because we could simply hard code it as okay if it's a simple if condition saying, if it's got more than the amount of the Mac tokens can handle, then summarize. That's the simple sort of sort of thing. But this way allows us to kind of programmatically and easily modularize it."

**Maintainability Advantage:** "and we could pull all that code out, change that code without changing anything else in the overall architecture of the application."

---

## Module 6: Summarizing Chatbot Class
**[1157.63s → 1888.16s]** *Main application class implementation*

### Lesson 6.1: Class Architecture Overview
**Timestamps:** [1157.63s → 1218.53s]

**Class Introduction:** "So now to utilize these functions, we're building basically a class called summarizing chatbot. So I'm going to kind of utilize. And this is kind of the main meat of the actual application itself."

**Core Functionality:** "So now this summarisation chatbot, or summarising chatbot rather, is a chatbot the user AI to generate responses, summarise conversation history, so we can say, hey, can you summarise everything we spoke about today in a single summary? and assess conversational complexity dynamically."

**Feature Integration:** "So that's the reason why we're making these sort of functionalities to kind of give this some sort of utility as such. Without making tooling, because we'll talk about tooling further on down the line."

### Lesson 6.2: Class Initialization
**Timestamps:** [1218.53s → 1319.70s]

**Initialization Parameters:**
- **Engine Parameter:** "And for the initialization, all we're doing is we're taking in an actual engine. We're hard coding that to be chatgeed to turbo 3.5."
- **History Length:** "We're taking a base history length, as you can see, only try to keep it safe. a base history of 10. If it gets to 10, we don't want to keep pushing it. But you could change that to 100, you could change to 50, you could change it to five, and you can kind of decide on that."

**Parameter Explanation:** "So this one is going to initialize a new instance of the summarizing part. So the first parameter again, I'll just explain, it's going to be the engine. Second, we're going to be the length, which is based on the base number of exchange before considering, hey, I need to summarize if I sort of like end up with more than 10 bunches of information to spit out."

**Instance Variables Setup:** "So here we're just literally setting up the OpenAI engine, the chat history, we're just storing it as a list for the moment, you might wanna make some more dynamic sort of thing to hold it."

**Storage Alternatives Discussion:** "You could use some sort of memorization, you could use a whole database, like graph database, but again, because we haven't actually covered that in any of our material just yet, we're sticking with simple and basic to use things that you can just swap that out for."

**Extensibility Note:** "That could be swapped out for a whole API and a connection set to go to any data you like. Then we'll give it the base history length which will pull from this parameter."

### Lesson 6.3: Get Response Method
**Timestamps:** [1319.70s → 1427.67s]

**Method Purpose:** "We've got to get response. So basically this is just gonna take some input text in. It's going to process the user input. It's going to generate some sort of response and update the conversation history."

**Parameter and Return:** "And the parameters again, is just the input text, which is basically the user input, with which the bunch then responds to. It's going to return the generator response from the bot."

**History Integration:** "So this is kind of utilizing that whole idea of history here. So first, we're going to take all the current chat history, join it together, via new lines. So we're just going to have all the chat history going to be on its own line."

**Prompt Construction:** "Then we're going to make our prompt be the chat history, but then add the user prompt being the input text. And then what we're going to do is we're going to have the bot preceded with the word bot so that when it's responding, we kind of have in the conversation where the user is whatever you put in and the bot is basically going to be talking back to you with the response."

**Response Generation:** "So then we utilize this utility function of generate response, given the prompt that's been taken from this prompt here, and then also passing the open AI engine so we have access to the engine."

**History Update:** "So we've already gone over what that function does, so now programmatically this will give us a response, but then what we'll do is we'll add the response to our history. We haven't spoken about what the update history does yet, but we'll kind of get to that in a moment, but in essence it just adds it to this list pretty much."

**Final Steps:** "So we take our input text and the response and add it as to this list of conversation history. Then we just return the response. So it's fairly straightforward again."

### Lesson 6.4: Update History Method - Core Logic
**Timestamps:** [1433.72s → 1525.21s]

**Method Purpose:** "Then we've got the update history. So the thing that this course here, this updates the conversation history with the latest exchange and manage its length. So if it gets too long, we kind of want it to go, no, no, this needs to summarize. We need to summarize something here."

**Parameters:** "So this takes the user input, which is whatever the latest input from the user is, and then the bot response as well."

**History Extension:** "So here we're going to say self.chat.history.extend. So we're kind of adding this list of things to the current list. That's all we're doing."

**Python List Operation:** "Those you do not use to Python, this is kind of fairly straightforward and I think but it literally just takes this list, takes the previous list and pretty much concatenates the two lists. And once it's done that, we now have a longer history with the current things."

**Complexity Check:** "But then what we want to do is we want to figure out is it too complex? Does it take up too much space and is it going to be causing us problems then line? So we've run the assess complexity, free standing function on it. And we pass it, the chat history, we also pass it the engine. This then gives us a complexity score."

### Lesson 6.5: Adaptive History Length Calculation
**Timestamps:** [1512.45s → 1572.62s]

**Decision Point:** "Then we need to decide on, well, is the score bad or good? So now we need to make an adaptive history length."

**Length Calculation:** "So we take a max of the current length, and then we pass it the min of either fifth day or the complexity score divided by five."

**Purpose Explanation:** "So this is a simple way of checking shall we kind of chop off some of this history and just basically turn it into summarisation of itself rather than kind of having it as its full text."

**Summarization Trigger:** "And then we go, if the length of our chat history longer than the adaptive history length times two, then we want to summarise the history."

**Summarization Process:** "So we say, summarise the text and join it by space, pass it the chat history and also pass it the engine, which is the particular one that we've got set."

**History Reset:** "Then what we do is we reset the chat history to be the summarised history."

### Lesson 6.6: History Restructuring Logic
**Timestamps:** [1572.62s → 1642.76s]

**Concatenation Process:** "and here we're doing something similar to how we did the extend, but it's hard coded to concatenate it. So all we're doing is we're taking this summarized history, turning it into a list, full of that summarized history."

**Recent History Preservation:** "Then we're adding the chat history, but we're adding it basically to the end of the thing. So we're adding the end of the chat history here, look. So we're starting at negative adaptive history length divided by two."

**Slicing Explanation:** "So we take whatever the adaptive history length is, we divide it by two, we negate it and turn it into a negative start. So we're starting from the other end, not the front. So it's almost like we're reversing it here. And then we're going to end. So we're kind of moving through."

**Final Result:** "So we're concatenating and adding the chat history there. So this is basically just adding all the summarizations to the history."

### Lesson 6.7: Student Questions on Adaptive History
**Timestamps:** [1642.76s → 1888.16s]

**Clarity Question:** Student: "I don't really understand what the point of the adaptive history length is."

**Length Adaptation Explanation:** "So basically the history, this was added as a thing so that we can make the history check the current adaptive history length. How long is it right now? And we want to be able to adapt that length."

**Detailed Scenario:** "So we're checking the current length, the base length, which our purpose is what 10. So if the current base length is greater than either 50 or our complexity score divided by 5 then we're going to set it to that. Otherwise we're going to be setting it, we're just going to leave it as it is basically, it's going to just set to that."

**Complex Example:** "So imagine the history contains, let's say, imagine the history has a score of 500. So if we do 500 divided by 5, that means that our complexity score is going to be 100, which is far too complex. It's more complex than we want it to be"

**Threshold Relationship:** "Yeah, so the moment we only want it to have imagine the base history length being its complexity score That makes it so this is its base. This is it's complexity This is a complexity what we want it to be But at this point we're checking is it like if that was a 10 is it five times the current complexity Or is it more than five times going complexity? If it is, then what we want to do is kind of like set that to the thing to chop it."

**Production Context:** Ash added: "It's also about efficiency because sometimes what happens is most implementations of summarization but you'll see on the internet today will take the full chat history and re-putting, whether it's a system prompt or an assistant prompt. Instead, if you make it adaptive, then you can continuously change when the complexity of the actual messages gets to a point that's a tipping point."

**Real-World Application:** "That's actually what we do with our technical tutor inside LoomTech for the other side of the school, where if it's a lot of back and forth questions, whether it's encoding or back and forth, we'll actually tip it over after a certain point of complexity and then summarize it."

**Alternative Message Types:** Student question about using different message types: "100%. You could 100% use different types of messages to make this three times better by saying, okay, you're gonna be this role, you're gonna be that role or the assistant message could be different or your user message could be delineated."

---

## Module 7: Advanced Implementation Discussion
**[1888.16s → 2247.16s]** *Performance optimization and LangChain alternatives*

### Lesson 7.1: Multiplier Logic Clarification
**Timestamps:** [1892.01s → 1989.92s]

**Follow-up Question:** Student: "then why are we multiplying it by two in the following line?"

**Performance Tuning Explanation:** "So, look, if the length of the chat history is greater than the adaptive history length, so realistically, the chat history's probably gonna be bigger than just the length anyway. So it won't, in this situation, we've kind of done a little bit of math under the hood and tweak this a few times and this seemed to be the sweet spot for the performance."

**Empirical Approach:** "And when you're actually building these out, it will be a case of a little bit of test it and remedial in test it. And this seems to be around about where it kind of works like performance at the time. So it's again, another little performance tweak that was just purely."

**Alternative Implementation Discussion:** Ash: "I also think that, whether complexity function, you could have also asked the LLM, just give me a guess or no, if I should summarize or not. You could have done that as well. So why do we choose a number instead of just saying yes or no?"

**Granularity Benefits:** "I think the all process there was, the number gives way more detail as to like whether or not you should go in one direction or not. Right now I've just made it 50. That's just because we're trying to keep it real simple to show you guys, but the thought process here is, but you guys can play with that."

**Flexibility Advantages:** "Maybe you want to do at 70. Maybe you want to do it at 20, maybe you want to do a 30. Maybe you actually want to do an actual API that judges complexity better. Maybe you make it a little bit more advanced. Maybe you make it way more simple. I just do yes or no. But the good part about this is if you make it adaptive, it'll be efficient. You'll save a lot of money too."

### Lesson 7.2: Student Alternative Implementations
**Timestamps:** [2054.88s → 2122.23s]

**Implementation Approaches:** Ash: "Did anybody do it in another way? I did see Chris's length chain one. So I have a suggestion for that. But did anybody else do it natively in OpenAI and take a different approach?"

**TikToken Library Usage:** Student: "I took it as we did using the library called TickToken. which is a tokenizer to pound the tokens. For the company's discourse."

**Vectorization Question:** "Did you vectorize and put in database? Or did you just chunk it up?"

**Encoding Method:** Student: "So it has a method called encoding for model. I'll be honest, I don't know what exactly it does."

**Future Integration:** Ash: "So next Tuesday, we'll be using TikTok in with pine cone to chunk it and then embed it and then send it to the vector database. So that's a great start actually. So definitely keep investing in there."

### Lesson 7.3: LangChain Abstractions Introduction
**Timestamps:** [2125.23s → 2247.16s]

**LangChain Benefits:** "The only other thing I'll bring up is the Langshan example. Why do I love Langshan so much? There's so many abstractions you can just use out of the box."

**Built-in Memory Solutions:** "The one I want to show you guys is... It's conversation summary. Inside Langshan.memory, there's conversation summary memory and chat message history. You can use this out of the box and this makes your life 10 times easier."

**Automation Benefits:** "A lot of the things that we had to do manually here, Langshin has done for you within the package itself."

**JavaScript Support:** "There's another one I would like to mention as well, which is, if you are any of your JavaScript developers, it's also available in that."

**Summary Buffer Memory:** "The summary buffer. So this is where you, if you want a specific thing saved inside the actual summary, you can actually define what that is using buffer memory and back and forth, Lenshane let's you do that out of the box."

**Callback Functions:** "The other thing I want to say is, Lenshane offers callback functions where you can take information like the number of tokens used, or the number of estimated number of money you use, and you can actually get that information out."

**Cost Management Application:** "So a lot of people were, we were talking about, hey, if you want to keep the token usage efficient, that's why we're summarizing and trying to make an adaptive. You can actually make it directly related to the actual number of tokens related or the actual amount of money being used back and forth by the chatbot."

**Production Use Cases:** "I think that is very useful, especially if you're making something where a lot of people are using your chatbot back and forth, like a support bot, or in our case, I'm going to check AI tutor."

---

## Module 8: Cost Management & Monitoring Tools
**[2252.96s → 2438.48s]** *LangSmith and observability platform comparison*

### Lesson 8.1: Token Charging Model
**Timestamps:** [2252.96s → 2284.36s]

**Student Question:** "Yeah, I charged for the amount of tokens returned by the model or are you charged for the whole context window?"

**Charging Clarification:** "And they can be in the previous part of the whole context window, but I will double check and make sure, but I do believe it is the full context though, that you are using when you send a message."

**Transition to Monitoring:** "But this is a great transition to what we're gonna be talking about tomorrow, which is LangSmith."

### Lesson 8.2: LangSmith Introduction
**Timestamps:** [2284.36s → 2332.00s]

**Platform Purpose:** "So LangSmith is a monitoring and managing tool for LLM applications and Nick, it actually calculates how much you're spending on every single LLM interaction and actually shows you how much you're spending as a whole on your application."

**Alternative Platforms:** "Now, there's three alternatives to Langsmith, and I'll talk about why we've chosen Langsmith over the other three."

**LangFuse:** "There's Langfuse, which is an open source alternative. This is pretty much the same as Langsmith, but it's open source."

**GenTrace:** "There's GenTreece"

**DataDog:** "and then DataDog just announced today that they're coming out with LLM observability inside of their platform. So a lot of our core one members were actually already using DataDog, so they were really excited for this."

### Lesson 8.3: Platform Selection Rationale
**Timestamps:** [2332.00s → 2417.88s]

**LangSmith Selection Reasons:** "So I'm gonna talk through why we've chosen Langsmith. The reason we've chosen Lengsmith is because it integrates into the Lengshade ecosystem seamlessly, really simply. All you need is one API key."

**Integration Simplicity:** "And if you put it within your environment, everything is tracked without you having to do much. Anytime it picks up a Lengshade library, anytime it picks up any LLM usage, it will track that for you out of the box."

**Privacy Concerns:** "Now a lot of you might be thinking, hey, Ash, I don't want to use Lengsmith because it's whatever. It's an internal private, whatever. So then, link use does the same, but it does have some functionality, it does not have some functionality."

**Missing Features in LangFuse:** "And what is the functionality that it does not have? It's annotating and making your own data sets. So we'll see tomorrow with Langsmith, you can actually pick and choose outputs, annotate them, and then save it to personalized data sets that you can then use in the future for fine tuning."

**Decision Factors:** "So that's probably one of the two big reasons where we've chosen Langsmith, but we will be introducing the Langfuse and Langsmith tomorrow as choices for you to use in the course."

**GenTrace Positioning:** "Now, GenTrace is up and coming, they just started out. You can pretty much do everything that you could do out of the box with Langsmith, accept the whole annotation and dataset creation. And if you're using Lama Index, this would be a better tool for you as it incorporates into Lama Index better."

**DataDog Status:** "And then obviously DataDog was something I just mentioned. They just announced beta, so I haven't actually tried that yet."

### Lesson 8.4: Course Progression Overview
**Timestamps:** [2420.68s → 2438.48s]

**Tomorrow's Preparation:** "So I did want to introduce that before tomorrow. I actually put some links out here for you guys to watch before the lecture tomorrow. So you guys can sort of just get to know it a little bit before we get into it."

**Course Trajectory:** "After lengthsmith on Tuesday, we hit the ground running officially with RAG and actually go into the techniques that are very important for creating these applications."

---

## Module 9: Production Considerations & Advanced Topics
**[2453.97s → 2943.87s]** *Real-world applications and future directions*

### Lesson 9.1: Code Repository and Resources
**Timestamps:** [2453.97s → 2480.04s]

**Implementation Access:** "And then the code is already available to you. It's in a branch called 24A2 I believe. I'm just going to check and make sure I'm correct on that. So you can see the full implementation right here that Tom walked you through and then we have a little setup guide for you as well."

### Lesson 9.2: Tool Ecosystem Summary
**Timestamps:** [2485.88s → 2536.52s]

**Platform Clarification:** Student: "So okay so we have Lang Smith, we have Lang Chen, we have Lang Hughes, and we have that Jen, that last thing you've shown."

**Course Focus:** "But for now, we should just read on Lensmiths... So just for now, do the links I showed you, I will be posting. OK, we've picked a path in this course. That's our opinion as the best text that currently. But it's important that we expose you to the alternatives."

**Tomorrow's Plan:** "So tomorrow, we'll be focusing on Langsmith and Langfuse. but I will definitely send you information on gentrists."

### Lesson 9.3: Student Feedback on Course Direction
**Timestamps:** [2554.10s → 2645.12s]

**Improvement Suggestion:** Student: "Obviously, this was fairly simplistic because we're at the start of things, but is there anything where you'd like to go in a more deep dive... is there anything, what would be a more complex sort of summary thing or is there something you'd like to kind of see in this portion of the course in the future."

**Developer Productivity Focus:** Student response: "Well, maybe it's mapping this to how it can be utilized for specifically for developer productivity. But I understand that you have to build the foundation first."

**Guided Project Integration:** Ash: "So yeah, I think every guided project will directly address developer productivity. And then everything leading up to it is going to be just setting up the stage for that guided project."

**Next Week's Project:** "So next week is the technical writer agent, which should aims to completely automate documentation creation. I mean, cohort one has taken it in several different directions."

**Live Project Access:** "By the way, that link is live right now. So if you want to look at that project, you can on the app.plumtech.com. and you can look at the starter repo for that, but I 100% agree with you. We will make sure that every guided project directly addresses developer productivity."

### Lesson 9.4: Course Design Philosophy
**Timestamps:** [2645.12s → 2692.24s]

**Feedback Loop Importance:** Tom: "Yeah, an awesome question. I'm sorry, awesome observation. Yeah, because I mean, it's best to kind of in these situations keep tight feedback loop because your answers will also help future people doing this course as well."

**Iterative Improvement:** "Because we like to kind of reiterate and make sure that everything is on point. It's always hard to get that balance of technical and simple to read and simple to look at."

**Diverse Student Backgrounds:** "You get different people from different walks of life coming in and you'll have varying technical abilities in the classes. Something that might work for this cohort may not work for next cohort if they have a different set of technical abilities. We have to find tune it in those ways as well."

### Lesson 9.5: Conceptual Understanding Questions
**Timestamps:** [2692.24s → 2802.17s]

**Application Beyond Chatbots:** Student: "We don't really conceptualize this in use. We are talking about a way to keep the size of a context down. But we also do this besides in chatbots."

**Context Window Management:** Student: "And then another question is something that I didn't really understand is, are we, if we're summarizing squashing history into a summary, are we reinitializing in instance, like a new context window with the model and sending it in the summary or we just rehashing like that."

**Context Preservation Explanation:** Tom: "We're doing, we're keeping the same context window because we're keeping the history. That's what's keeping the context, our code is keeping the context. So basically it is kind of a new context window, but because we've got the history, it's keeping that set. but then it's also changing it out to summary so that we're not using as much tokens of those data things as we do."

**RAG Application:** Ash: "Okay, and then a more ap another practical application for the summary is when you're ragging something, so in the future we'll talk about this. Let's see you're ragging 100 documents. Instead of looking through every single document when the AI is trying to decide where to rag from, the AI will summarize every single document and have summaries on top so it can query based on the summary much quicker than it can then reading the whole document."

### Lesson 9.6: Production Implementation Strategies
**Timestamps:** [2814.19s → 2891.20s]

**Information Loss Concern:** Student: "So in an actual production environment, you would want a more advanced approach because the summarization might lose something that you actually consider important. So I guess in practice, would you use some sort of an agentic approach where you queries a summary and then that doesn't have an answer you do IRG and then that is where it works for you, try to feed the whole contact purge. Is there a multi-layered approach?"

**LangGraph Solution:** Ash: "In production, we would use something called Langgraph. Langgraph has memory built in to the agent scratch pad. So this is pushing ahead, but Langgraph, what it does is it'll help you create that mechanism of decisions, and that mechanism of maintaining memory across the entire, I guess, generation chain."

**Memory Preservation:** "And so once that generation is complete, then you're able to then maintain that memory without having anything to lose. So the answer is, how do you do it in production? You use Lenggraph, but and there are definitely methods that are we'll talk about how to make sure that accuracy is good."

**Future Integration:** "But next week, we'll talk about just using some resets of holes, so just locally not in production... And it's a combination of Korea and Leng, which is a week seven, I think, seven, right?"

### Lesson 9.7: Session Wrap-up
**Timestamps:** [2910.23s → 2943.87s]

**Final Logistics:** Ash: "Okay, the only other thing is I'm going to post a Lune video mid-day tomorrow, maybe early morning. I have the video already. I just don't want to bombard you guys with emails and slack messages."

**Setup Video Content:** "So you guys, I hate Ash, just keeps emailing me. But the video is just how to set up an account on Langsmith just to make sure you guys have that ready to go before class. It takes all of two minutes."

**Session Conclusion:** "And so that'll be the only thing I go over. Besides that, I hope you have a great day. So talk to you you guys tomorrow, if you haven't, thank you."

---

## Key Teaching Methodologies Observed

### Interactive Problem-Solving Approach
- **Live Coding:** Step-by-step implementation with real-time explanation
- **Student-Driven Questions:** Encouraging clarification and alternative approaches
- **Practical Focus:** "This was just for this simple explanation and demonstration"
- **Modular Teaching:** Breaking complex functionality into discrete, reusable functions

### Production-Readiness Awareness
- **Version Management:** Acknowledging OpenAI library version differences
- **Best Practices:** Distinguishing between development shortcuts and production approaches
- **Real-World Integration:** Connecting classroom concepts to actual BlumeTech implementations
- **Tool Ecosystem:** Comparing multiple platforms (LangSmith, LangFuse, GenTrace, DataDog)

### Scaffolding Techniques
- **Foundation First:** "We haven't gotten to that content yet in the syllabus"
- **Progressive Complexity:** Starting with simple functions, building to complete applications
- **Alternative Implementations:** Discussing both manual approaches and framework abstractions
- **Future Connections:** Linking current concepts to upcoming course topics (RAG, LangGraph)

This comprehensive recreation captures the complete teaching experience, preserving all technical implementations, student interactions, design decisions, and pedagogical approaches used throughout the 49-minute office hours session.
