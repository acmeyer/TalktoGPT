# TalktoGPT

This repository is a project that allows you to talk to ChatGPT with your voice and get audio responses back.

## Setup

To get running quickly, install all the dependencies:

```
pip install -r requirements.txt
```

Next, you'll have to set up authentication with the two APIs from Google and OpenAI.

### Google Cloud

To use the Google Cloud Speech to Text API, you'll need to set up authentication. You can do that by downloading a service account key from the [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts). Once you have the key, set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the key file. For example:

```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

### OpenAI

To use the OpenAI API, you'll need to set up authentication. You can do this by following the instructions [here](https://platform.openai.com/docs/api-reference/authentication). But the easiest way is to just set the `OPENAI_API_KEY` environment variable to your API key. For example:

```
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## How to Use

The simplest way to get started is by running:

```
python main.py
```

However, you can customize the settings more with the following command line arguments:

- `--stop_word`: The word that will stop the conversation. Default is `bye`.
- `--voice`: The voice to use for text to speech. Default is `Google`. The only other option right now is `macOS`, which will use the default macOS voice. The advantage of this one is that you don't have to pay for it but it is pretty robotic.


## Potential Improvements

In order to do the quickest and dirtest version of this, I utilized available APIs from OpenAI and Google. However, there is a way to do all of this locally on your machine (though, for now at least, you'll likely see worse performance). One example of using local machine instead of APIs is the option to use the native `macOS` voice instead of Google Cloud's text to speech API.

Here's what could be done with a bit more effort to get this same concept running entirely on your local machine, without relying on any APIs:
1. Pick an open source model to use instead of ChatGPT. One option is [llama.cpp](https://github.com/ggerganov/llama.cpp)
2. Choose an open source model for text to speech, like Whisper's open source version. Here's an option you can use locally [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
3. While this project does have the option to use the native macOS voice, it's not the best one. You could replace it with another locally hosted one.