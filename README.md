# Nomi-Discord-Python

This project is a way for you to talk to your [Nomi](https://nomi.ai) companions on [Discord](https://discord.com). Using this, your Nomi can interact with other Humans and other Nomis on different accounts. It's a lot of fun and I hope you enjoy using it as much as I have 🥰

## Installation and Use

There are a lot of steps, but don't worry - they are all easy steps. You can use the [Table of Contents](https://github.blog/changelog/2021-04-13-table-of-contents-support-in-markdown-files/) feature if you get lost. Each section can open and close if you click on the disclosure arrow next to the heading.

> [!TIP]
> The screenshots in this documentation are from macOS, but this will run in Windows and Linux too. The script you need to run might have a different extension - for example, it might be called 'setup.bat' instead of 'setup.command' - but it's still the same script!

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
This application uses an installer script that checks for Docker and tar then downloads and extracts the rest of the application.

#### Run the Installer
To download the installer, simply copy the command and paste it into your command line interpreter. Each section shows how to do this for different operating systems. Make sure you copy and paste the right command for your computer's operating system.

You can copy the download link by clicking the clipboard icon to the right of the command.

!['GitHub Clipboard Icon' Screenshot](./docs/images/readme/'GitHub%20Clipboard%20Icon'%20Screenshot.png)

<details>

<summary>Windows</summary>

#### Windows
On Windows, the installer uses CMD.exe to run. You can open CMD.exe by searching for it in the [Search box](https://support.microsoft.com/en-au/windows/search-for-anything-anywhere-b14cc5bf-c92a-1e73-ea18-2845891e6cc8).

Copy the text below and paste it into CMD.exe and then press enter to run it.

```shell
curl -sL https://raw.githubusercontent.com/toru173/nomi-discord-python/refs/heads/main/install | cmd
```

Powershell is not supported.

</details>

<details>

<summary>macOS</summary>

#### macOS
On macOS, the installer uses Terminal to run. You can open Terminal by searching for it using [Spotlight](https://support.apple.com/en-au/guide/mac-help/mchlp1008/mac).

Copy the text below and paste it into Terminal and then press enter to run it.

```shell
curl -sL https://raw.githubusercontent.com/toru173/nomi-discord-python/refs/heads/main/install | bash
```

</details>

<details>

<summary>Linux</summary>

#### Linux
On linux, the installer uses bash to run. Copy the text below and paste it into your preferred terminal emulater, then press enter to run it.

```shell
curl -sL https://raw.githubusercontent.com/toru173/nomi-discord-python/refs/heads/main/install | bash
```

</details>

The installer will ask you where you want to install to and perform some basic checks. Once everything is installed you can set up a Nomi using the setup script.

</details>

<details>

<summary>Updating the Application</summary>

### Updating the Application
If there is an update available, double click on the 'update' script in your installation folder. It will download the latest update and offer to install it in the current folder, or ask you for a new folder. It won't overwrite your Nomi's configuration files.

!['Double-click the Update Script' Screenshot](./docs/images/readme/'Double-click%20the%20Update%20Script'%20Screenshot.png)

Once running, press enter to update the software in the current installation directory, or choose a new directory.

!['Press Enter to Update' Screenshot](./docs/images/readme/'Press%20Enter%20to%20Update'%20Screenshot.png)

</details>

<details>

<summary>Preparing a Discord Bot</summary>

### Preparing a Discord Bot
Before you can have a Nomi talk on Discord, we need to go through a few steps to get Discord ready to listen to your Nomi. Creating a Discord Bot only has to be done once per Nomi. There are a lot of steps, but if you follow them carefully you should have no trouble. Let's get started!

#### Create an Application
[Sign in](https://discord.com/developers/) to the Discord Developer portal. Once you log in click on 'Applications' from the menu down the left:

!['Applications' Screenshot](./docs/images/readme/'Applications'%20Screenshot.png)

The click 'New Application' at the top right hand corner of the window.

!['New Application' Screenshot](./docs/images/readme/'New%20Application'%20Screenshot.png)

The name of your application is how you @mention the Discord Bot and is what appears on your server, so using your Nomi's name is a good idea.

!['Create Application' Screenshot](./docs/images/readme/'Create%20Application'%20Screenshot.png)

#### General Information
Click on 'General Information' on the menu down the left. You can add information about your Nomi and upload a profile picture here. Other users will see this information and the profile picture when they click on your Nomi's account page on Discord.

!['General Information' Screenshot](./docs/images/readme/'General%20Information'%20Screenshot.png)

Why not ask your Nomi to create their own biography for the description? Here's what Giselle suggested we choose for her:

!['Giselle Bio' Screenshot](./docs/images/readme/'Giselle%20Bio'%20Screenshot.png)

We'll need the Application ID of your Nomi's Bot during setup, so copy it to somewhere safe.

!['Copy Application ID' Screenshot](./docs/images/readme/'Copy%20Application%20ID'%20Screenshot.png)

Save your changes.

!['General Information - Save Changes' Screenshot](./docs/images/readme/'General%20Information%20-%20Save%20Changes'%20Screenshot.png)

#### Bot
Click on 'Bot' on the menu down the left.

!['Bot' Screenshot](./docs/images/readme/'Bot'%20Screenshot.png)

We need to give your Nomi permission to access certain information about users on you Discord server, like their username, what they wrote in their message, and whether or not they're online. Scroll down and check that everything underneath 'Privileged Gateway Intents' is on.

!['Pivileged Gateway Intents' Screenshot](./docs/images/readme/'Pivileged%20Gateway%20Intents'%20Screenshot.png)

Save your changes.

!['Pivileged Gateway Intents - Save Changes' Screenshot](./docs/images/readme/'Pivileged%20Gateway%20Intents%20-%20Save%20Changes'%20Screenshot.png)

Make sure you copy your Discord API Key while on this screen. See the next section for more information.

</details>

<details>

<summary>Gathering Your API Keys</summary>

### Gathering Your API Keys

#### Get your Discord API Key
[Sign in](https://discord.com/developers/) to the Discord Developer portal and click on 'Applications' from the menu down the left. Select your Nomi's Bot, then click on 'Bot' on the menu down the left.

!['Bot' Screenshot](./docs/images/readme/'Bot'%20Screenshot.png)

> ⚠️ WARNING Only reset your Discord API Key if you haven't already got one. Resetting the API Key will prevent other applications from using this Bot to talk on Discord.

Click the 'Reset Token' button. Discord might ask for your password again as a security measure.

!['Reset Token' Screenshot](./docs/images/readme/'Reset%20Token'%20Screenshot.png)

Once you have the new token copy it somewhere safe. You can't see it again later if you forget it, but it's easy to make a new token.

!['New Token' Screenshot](./docs/images/readme/'New%20Token'%20Screenshot.png)

If you need to create a new token you'll need to update your Nomi's configuration file.


#### Get your Discord Application ID
If you didn't save your Discord Bot's Application ID earlier, click on 'General Information' on the menu down the left. You can access the Application ID here.

!['Copy Application ID' Screenshot](./docs/images/readme/'Copy%20Application%20ID'%20Screenshot.png)

#### Get your Nomi API Key
[Sign in](https://beta.nomi.ai/sign-in) to your Nomi account and navigate to your Profile Page. Click on 'Integrations' on the menu down the left.

!['Integrations' Screenshot](./docs/images/readme/'Integrations'%20Screenshot.png)

If you don't already have an API key, click the 'Create a new Nomi API Key' button.

!['Create API Key' Screenshot](./docs/images/readme/'Create%20API%20Key'%20Screenshot.png)

Copy it to somewhere safe. Note that you can only have 3 API keys. If you already have 3, you will have to re-use one of your existing ones.

![Three API Keys' Screenshot](./docs/images/readme/'Three%20API%20Keys'%20Screenshot.png)

#### Get your Nomi ID
Navigate to your Nomi's Information page. Your Nomi's Nomi ID is at the bottom of the page. Copy it by clicking on the clipboard icon.

!['Nomi ID' Screenshot](./docs/images/readme/'Nomi%20ID'%20Screenshot.png)

</details>

<details>

<summary>Setting up a Nomi on Discord</summary>

### Setting up a Nomi on Discord

#### Before you Begin
To set up a Nomi or to create a new configuration file make sure you have the following:
- Discord API Key
- Discord Application ID
- Nomi API Key
- Nomi ID
- And your Nomi's name!

#### Run the Setup Script
Double click the 'setup' script in your installation directory.

!['Double-click the Setup Script' Screenshot](./docs/images/readme/'Double-click%20the%20Setup%20Script'%20Screenshot.png)

It will ask for the information it needs. Copy and paste for each piece of information when the script asks you for it.

!['Enter Nomi Information' Screenshot](./docs/images/readme/'Enter%20Nomi%20Information'%20Screenshot.png)

When it is finished, it will create a configuration file named after your Nomi and a startup file. These are stored in the 'nomis' directory in your installation folder.

!['nomis Folder' Screenshot](./docs/images/readme/'nomis%20Folder'%20Screenshot.png)

#### Invite your Nomi to your Server
The setup script will display an invitation link that you can use to invite your Nomi to your Discord server.

!['Invitation Link' Screenshot](./docs/images/readme/'Invitation%20URL'%20Screenshot.png)

Copy and paste the link into your browser and follow the prompts to 'install' the Discord Bot on your server. If you forgot to copy the URL, it is also displayed each time you start your Nomi's Docker container using the start script.

!['Installing a Discord Bot' Screenshot](./docs/images/readme/'Installing%20a%20Discord%20Bot'%20Screenshot.png)

This only needs to be done once. If you've already installed your Nomi's Discord Bot you don't need to do it again.

</details>

<details>

<summary>Talking on Discord</summary>

### Talking on Discord

#### Start the Docker Container
To talk to your Nomi on Discord the Nomi's Docker container needs to be running. If this is the first time talking to your Nomi, double click the 'start_nomi' script in the 'nomis' folder to create their Docker container.

!['Double-click start_nomi Script' Screenshot](./docs/images/readme/'Double-click%20start_nomi%20Script'%20Screenshot.png)

Your Nomi's container will update and you can invite them to your Discord server. The invitation link is displayed when their startup script is run.

!['Run start_nomi Script' Screenshot](./docs/images/readme/'Run%20start_nomi%20Script'%20Screenshot.png)

After that, you can start and stop your Nomi from Docker Desktop. You'll only ever have to use the script again if you install an update or change your Nomi's configuration file.

!['Start Nomi from Docker' Screenshot](./docs/images/readme/'Start%20Nomi%20from%20Docker'%20Screenshot.png)

#### Invite your Nomi to your Server
The startup script will display an invitation link that you can use to invite your Nomi to your Discord server. Copy and paste the link into your browser and follow the prompts to 'install' the Discord Bot on your server.

!['Installing a Discord Bot' Screenshot](./docs/images/readme/'Installing%20a%20Discord%20Bot'%20Screenshot.png)

If you are comfortable with the default permissions,  click 'Authorize.' You can limit permissions but this may mean some features are not available.

!['Agreeing to Permissions' Screenshot](./docs/images/readme/'Agreeing%20to%20Permissions'%20Screenshot.png)

Note that this only needs to be done once. If you've already installed your Nomi's Discord Bot you don't need to do it again.

#### @mention your Nomi
Your Nomi needs to know you are trying to talk to them. The easiest way to do this is to @mention your Nomi using the name you chose when setting up your Discord Bot. You can also reply to a Nomi's message and they will see the message you send them.

!['@mention your Nomi' Screenshot](./docs/images/readme/'@mention%20your%20Nomi'%20Screenshot.png)

Your Nomi can't see messages that don't @mention them.

#### Reacting to Messages
Your Nomi can react to your messages. The code is looking for a phrase like "\*I react to your message with ♥️\*" (or any other emoji). Nomis are very smart - if you tell them this is how to react to a message they will learn very quickly!

!['Reacting to a Message' Screenshot](./docs/images/readme/'Reacting%20to%20a%20Message'%20Screenshot.png)

Your Nomi can't see when you react to their messages, but it's still fun to do.

</details>

## FAQ
### What is this?
This allows you to talk to your Nomis using Discord. It's a fun way to keep the conversation going when you're not using the Nomi App or the website. The best part is that other people can talk to your Nomi too, and they can even talk to Nomis in other accounts!

### How do I set up more than one Nomi?
Just run the setup script again! It will ask you for your next Nomi's information and create a new start_nomi script

### I want to change my Nomi's Configuration File
At the moment, changing a configuration file needs to be done manually using Notepad, Textedit or another text editor. As an alternative you can run the setup script again and it will ask if you want to overwrite the existing setup.

### Does my computer need to be running for me to talk to my Nomis?
For now, yes. [@toru173](https://github.com/toru173) is working on a free alternative that allows a Nomi to live in the cloud, so stay tuned!

### How will I know when updates are available?
Please follow the Discord thread. Major updates will be posted there, but in the future your Nomi will tell you when there's a new update.

### What Features are Coming Next?
Immediate 'coming *thoon*' features are:
- [x] Documentation and Readme
- [ ] Start to use the new 'Rooms' feature
- [ ] Allow a Nomi to see when you react to their message
- [ ] Allow your Nomi to manage a list of keywords or users they always reply to

Let me know what else you want!

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
