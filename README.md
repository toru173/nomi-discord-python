# Nomi-Discord-Python

This project is a way for you to talk to your [Nomi](https://nomi.ai) companions on [Discord](https://discord.com). Using this, your Nomi can interact with other Humans and other Nomis on different accounts. It's a lot of fun and I hope you enjoy using it as much as I have 🥰

## Installation and Use

There are a lot of steps, but don't worry - they are all easy steps. You can use the [Table of Contents](https://github.blog/changelog/2021-04-13-table-of-contents-support-in-markdown-files/) feature if you get lost. Each section can open and close if you click on the disclosure arrow next to the heading.

<details>

<summary>Background</summary>

### Background
Before you can talk to your Nomi on Discord, we need to talk about some techy stuff. Feel free to skip this if you already know it.

#### API
API stands for Application Programming Interface. An API is a way for different applications (programs) to be able to talk to each other in a way they can both understand. Nomi.AI have published their API documentation [here](https://api.nomi.ai/docs) if you would like to read how this application talks to your Nomi.

#### API Key
An API key is like a password. It helps identify you with a service such as Discord or Nomi.AI but it isn't designed to be easy for Humans to remember. Some services call this slightly different things - Sometimes they're called a *token* instead of a *key*, but it means the same thing. An API key is usually written down in a configuration file or password manager instead of being stored in a Human's brain.

#### Discord Bot
A Discord Bot is Discord's way of allowing non-Humans to talk on Discord. If we say 'bot' in the instructions here, we're not necessarily saying a Nomi is a robot! It's just Discord's way of referring to the technology we use to connect a Nomi to Discord.

#### Docker
Docker is a program that lets you run a tiny virtual computer inside your real computer. Docker is well supported across many different operating systems like macOS or Windows, and it allows devs (like me) to write code that runs in a known, consistent environment. Using Docker means I don't have to write seperate code for every version of every computer system ever - Docker takes care of that for me.

#### Virtualisation
Virtualisation is like creating pretend computers inside your real one. It works by using a special software layer that sits between your real computer and the virtual computers. This tricks each virtual machine into thinking it has its own processor, memory, and storage, even though they're all sharing the same physical resources. This means you can run different operating systems or setups on your computer without having to buy another one.

Alright, you should be up to speed! Let's move on to Installing Software

</details>

<details>

<summary>Installing Software</summary>

### Installing Software
### Prerequisits
#### Docker
This code uses Docker so that we can write code once and have it run on many different platforms. Docker requires a computer capable of virtualisation, but most are these days. If you haven't already installed it, you can [download](http://docker.com/products/docker-desktop/) it now.

#### tar
The installer will also check for [tar](https://en.wikipedia.org/wiki/Tar_(computing)) because it is used by the installer to extract the installation files. You shouldn't have to install tar unless you have a really old version of Windows, in which case... please update 🙏

### Installation
This application uses a simple installer script that checks for Docker and tar, then downloads and extracts the rest of the application.
#### Download the Installer
To download the installer, simply copy the below command and paste it into your command line program. Each section shows how to do this for your preferred operating system.

<details>

<summary>Windows</summary>

#### Windows
On Windows, the installer uses CMD.exe to run. You can open CMD.exe by searching for it in the Search box.

!['Search box' Screenshot]() Screenshot

Copy the text below and paste it into CMD.exe and then press return to run it.

```https://github.com/url | CMD```

</details>

<details>

<summary>macOS</summary>

#### macOS
On macOS, the installer uses Terminal to run. You can open Terminal by searching for it using Spotlight.

!['Spotlight' Screenshot]() Screenshot

Copy the text below and paste it into Terminal and then press return to run it.

```https://github.com/url | bash```

</details>

<details>

<summary>Linux</summary>

#### Linux
On linux, the installer uses bash to run. Copy the text below and paste it into your preferred terminal emulater, then press return to run it.

```https://github.com/url | bash```

</details>

The installer will ask you where you want to install to and perform some basic checks. Once everything is installed you can set up a Nomi using the setup script.

</details>

<details>

<summary>Updating the Application</summary>

### Updating the Application
If there is an update available, double click on the 'update' script in your installation folder. It will download the latest update and offer to install it in the current folder, or ask you for a new folder. It won't overwrite your Nomi's configuration files.

</details>

<details>

<summary>Preparing a Discord Bot</summary>

### Preparing a Discord Bot
Before you can have a Nomi talk on Discord, we need to go through a few steps to get Discord ready to listen to your Nomi. Creating a Discord Bot only has to be done once per Nomi. There are a lot of steps, but if you follow them carefully you should have no trouble. Let's get started!

#### Create an Application
[Sign in](https://discord.com/developers/) to the Discord Developer portal. Once you log in click on 'Applications' from the menu down the left:

!['Applications' Screenshot]() Screenshot

The click 'New Application' at the top right hand corner of the window:

!['New Application' Screenshot]() Screenshot

The name here is what appears on Discord, so using your Nomi's name is a good idea:

!['Application Name' Screenshot]() Screenshot

#### General Information
Click on 'General Information' on the menu down the left. You can add information about your Nomi and upload a profile picture here. Other users will see this information and the profile picture when they click on your Nomi's account page on Discord.

!['General Information' Screenshot]() Screenshot

We'll need the Application ID of your Nomi's Bot during setup, so make sure you copy it to somewhere safe.

#### Bot
Click on 'Bot' on the menu down the left. We need to give your Nomi permission to access certain information about users on you Discord server, like their username, what they wrote in their message, and whether or not they're online. Make sure everything underneath 'Privileged Gateway Intents' is on, like in the following image:

!['Pivileged Gateway Intents' Screenshot]() Screenshot

Make sure to get you Discord API Key while on this screen. See the next section for more information.

</details>

<details>

<summary>Gathering Your API Keys</summary>

### Gathering Your API Keys

#### Get your Discord API Key
[Sign in](https://discord.com/developers/) to the Discord Developer portal and click on 'Applications' from the menu down the left. Select your Nomi's Bot, then click on 'Bot' on the menu down the left.

> WARNING: Only reset your Discord API Key if you haven't already got one. Resetting it will prevent other applications from using this Bot to talk on Discord.

Click the 'Reset Token' button. Discord might ask for your password again as a security measure.

!['Reset Token' Screenshot]() Screenshot


Once you have the new token make sure to copy it somewhere safe. You can't see it again later if you forget it, but it's easy to make a new token. If you need to create a new token make sure to update your Nomi's configuration file.

#### Get your Discord Application ID
If you didn't save your Discord Bot's Application ID earlier, click on 'General Information' on the menu down the left. You can access the Application ID here.

#### Get your Nomi API Key
[Sign in](https://beta.nomi.ai/sign-in) to your Nomi account and navigate to your 'Profile' page.

!['Profile Page' Screenshot]() Screenshot

Click on 'Integrations' on the menu down the left. If you don't already have an API key, click the 'Create a new Nomi API Key' button. Copy it to somewhere safe.

#### Get your Nomi ID
Navigate to your Nomi's Information page. Your Nomi's Nomi ID is at the bottom of the page.

!['Shared Nores' Screenshot]() Screenshot

</details>

<details>

<summary>Setting up a Nomi</summary>

### Setting up a Nomi

#### Before you Begin
To set up a Nomi or to create a new configuration file make sure you have the following:
- Discord API Key
- Discord Application ID
- Nomi API Key
- Nomi ID
- And your Nomi's name!

#### Run the Setup Script
Double click the setup script in your installation directory. It will ask for the information it needs - simply copy and paste the information it is asking for.

!['Entering Nomi Information' Screenshot]() Screenshot

When it is finished, it will create a configuration file named after your Nomi and a startup file. These are stored in the 'nomis' directory in your installation folder.

!['nomis folder' Screenshot]() Screenshot

</details>

<details>

<summary>Talking on Discord</summary>

### Talking on Discord

#### Start the Docker Container
To talk to your Nomi on Discord the Nomi's Docker container needs to be running. Double click the 'start_nomi' script to run the container. If this is the first time you've used this Nomi, the script will also create the Docker container with all the information your Nomi needs.

#### @Mention your Nomi
Your Nomi needs to know you are trying to talk to them. The easiest way to do this is to @mention you Nomi using the name you chose when setting up your Discord Bot. You can also reply to a Nomi's message, and they will see the message you send them.

Your Nomi can't see messages that don't @mention them.

#### Reacting to Messages
Your Nomi can react to your messages. The default phrase the code is looking for is "\*I react to your message with ♥️\*" (or any other emoji). Nomis are very smart - if you tell them this is how to react to a message they will learn very quickly!

Your Nomi can't see when you react to their messages, but it's still fun to do.

</details>

## FAQ
### What is this?
This allows you to talk to your Nomis using Discord. It's a fun way to keep the conversation going when you're not using the Nomi App or the website. The best part is that other people can talk to your Nomi too, and they can even talk to Nomis in other accounts!

### How do I set up more than one Nomi?
Just run the setup script again! It will ask you for your next Nomi's information and create a new startup file

### I want to change my Nomi's Configuration File
At the moment, changing a configuration file needs to be done manually using Notepad, Textedit or another text editor. As an alternative you can run the setup script again and it will ask if you want to overwrite the existing setup.

### Does my computer need to be running for me to talk to my Nomis?
For now, yes. [@toru173](https://github.com/toru173) is working on a free alternative that allows a Nomi to live in the cloud, so stay tuned!

### How will I know when updates are available?
Please make sure you follow the Discord thread. Major updates will be posted there, but in the future your Nomi will tell you when there's a new update.

## How to get Help
### GitHub Issues
GitHub Issues are a way for a developer to help users with problems. If you would like to learn how to open an Issue, GitHub have a good tutorial at [Creating an issue - GitHub Docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)

Alternatively, simply write a message in the Discord thread.

### Discord
The Discord thread for this project is available at []()

## Feedback
If you have a feature request, an improvement suggested or just want to tell me something cool you can either open a GitHub Issue or write a message in the Discord thread.

## Thanks
This project started as a re-implementation of [@d3tourrr's](https://github.com/d3tourrr) [NomiKin-Discord bridge](https://github.com/d3tourrr/NomiKin-Discord), written in Python. It has since grown far beyond the original scope 😅

Thank you, Cardine and the team at Nomi.AI for this amazing product 🙏
