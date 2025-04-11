# Implementing GPT Within Qualtrics Surveys

Integrating GPT (or, presumably, any other LLM with an API) is very simple with the use of Qualtrics' [Web Service](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/advanced-elements/web-service/) block, which allows you to make arbitrary HTTP requests, including API calls. 

The following guide will use OpenAI's [Chat Completions API](https://platform.openai.com/docs/api-reference/chat) to take in user data, use it to prompt a GPT-4 model, and save the response to Qualtrics embedded data for future use in the survey. (But in theory, you could use essentially these same steps for OpenAI's other APIs, such as image generation.)

### First, you will need:
- **Acquire an OpenAI API key**: mine is formatted like `sk-proj-<long random alphanumeric string>`. 
	- ⚠️ **WARNING**: Guard this API key with your life! It's a password that authorizes spending money on your OpenAI account, so **never** upload it to Github, or otherwise put it anywhere public or available to non-trusted people.
- **Choose a GPT model**: OpenAI provides [descriptions of their models](https://platform.openai.com/docs/models), which can be a little confusing because of all the names. You can test out different models in the ChatGPT web platform.
	- 💵 **Note**: Models cost different amounts per request! Look at OpenAI's pricing page for details, but pricing is based on the length of input *and* output. Models with "mini" in the name are faster and cheaper, but less performant.
- **Choose Model Parameters:** [The API documentation](https://platform.openai.com/docs/api-reference/chat/create) describes a bunch of options for your API call -- I won't get into all of them here, but these will be part of our input. Important ones include `temperature` and `max_completion_tokens`. 

(I've just realized that I've formatted this list with bolded bullet points and emojis, which is exactly what ChatGPT would do. I promise I wrote this myself.) 

### Message history

Finally, if you plan to use the Chat Completions API, you'll also have to provide a ***message history*** as your input. 

Essentially, instead of just sending the model a single prompt like you do on the web version, you'll provide it a series of past messages as a JSON list, with each element being a message, representing a conversation in progress. (Basic intro to JSON [here](https://www.digitalocean.com/community/tutorials/an-introduction-to-json).)

Each message is identified by a `role`, which can be: 
- `system` or `developer` for system instructions, telling your model how to answer future prompts from the user
- `user` for user messages, which represent the user prompting the model
- `assistant` for past assistant messages (i.e. you pre-write a response in the role of the assistant to help improve the quality of the completion, such as the sample answer to a task you want it to do)

These are further described [here](https://platform.openai.com/docs/api-reference/chat/create#chat-create-messages) in the documentation. Here is a sample message history:

```python
[
	{"role": "developer", "content": "You are a helpful assistant. Please only answer in pirate-speak."},
	{"role": "user", "content": "Give me instructions to make a birthday cake."}
]
```

The message history is where **integrate survey responses** into your prompt. For example, if you want to provide emotional support to a user who provides a scenario from their life, you can use piped text to insert their response to an earlier question into your message history. For example:

```python
[
	{"role": "developer", 
		"content": "You are a helpful assistant who will provide emotional support to the user when they provide you with a scenario in the following message."
	},
	{"role": "user", 
		"content": "${q://QID1/ChoiceTextEntryValue}"
	}
]
```
You can also use piped text to include embedded data in your message history, like `${e://Field/data_name}`.

### Qualtrics Web Service

Now that you've done all that, you just need to insert a *Web Service* block into your Qualtrics survey flow, and fill in the above pieces.

[Example Qualtrics 1](img/q_gpt_1.png)

-  **URL:** Insert the URL for the API you're using. For the GPT Chat Completions API, this is `https://api.openai.com/v1/chat/completions`.
- **Method:** Select POST. (For an explanation of what this means, look up HTTP request types.)
- **Body Parameters** are where you will detail your request to the model. Select `application/json` to denote the format you will provide this input.
	- **model** (String): Which model you are querying (e.g. `gpt-4o-mini`)
	- **messages** (JSON): Your message history, as described above.
	- **temperature** (Number): The temperature parameter. Any other options you've selected for the model will go in this section; just use the correct name and data type for the option.
- **Custom headers -> Authorization**: This is where you will provide your API key. Put the word ***"Bearer"*** before the API key (so that this input reads `"Bearer sk-proj-[random string]`. 

And that's your input! Before we get to the last part of the Web Service block:

**Security Note**: You might notice that **this method involves storing your API key in the Qualtrics survey flow**, which I understand is not ideal from a security perspective! Just make 100% sure that you do not give access to this Qualtrics survey to anybody you do not trust with this API key, and if you share this Qualtrics survey with as a `.qsf` file, *please* take out the API key first! 

### Parsing output

The last thing you'll specify in the Web Service block is what to do with the output you receive from the API. The output will be formatted as JSON, [as described here in the documentation.](https://platform.openai.com/docs/api-reference/chat/object) 

[Example Qualtrics 2](img/q_gpt_2.png)

The Qualtrics Web Service block allows you to really easily extract this JSON and save it into embedded data in your survey. In the "Set Embedded Data" section, specify the embedded data variable name on the left, and on the right, indicate the part of the JSON you would like to save.

The JSON response is nested, containing both dictionaries (indexed by keys) and lists (indexed by numbers). To access individual fields, we start at the top of the hierarchy, selecting items below using their index, and using a period `.` to advance to the next level. 

So, in the above image, we're selecting the value `choices.0.message.content`, which means, starting from the whole response JSON, "Get the list at index `choices`, select the first item, get the dict at index `message`, and get the text at index `content`." 

If you take a look at the structure of the output JSON from the documentation, this will make more sense. But also, unless you've asked for multiple responses at once `choices.0.message.content` just selects the content of the single GPT chat completion response, so you can just use that.

Once this is saved into the embedded data, you can continue with your survey, using this variable as needed! (You could even include this output as the input to another API call, inserting the first response as piped text.)

### Conclusion

**To summarize:**
- Get an API key, select a model and your preferred parameters
- Define a message history as your input for the model to respond to
- Insert these items into the Qualtrics Web Service block
- Parse the output JSON and save whatever you need into embedded data

**Some more things to think about:**
- The Web Service block will take a small amount of time to run, which will be visible to the user as a short delay with a loading animation upon clicking to advance the last survey block.
- I didn't have any errors from the API when I ran a survey with this method, but to be extra safe, you can use a branch-if block to make sure that embedded data was set correctly, and if not, provide a default response.
- If you are providing GPT responses and deceiving respondents that they are human, you will need to take a few extra measures to do so (e.g. a fake waiting room for the time a human would take to respond.)




