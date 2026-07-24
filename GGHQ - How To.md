## So, you want to set up some Custom Liveries...

1. Design (or find an existing design of) a livery you like!

    There's tonnes of really good resources online showing you how you can create your own using GIMP/Photoshop etc.

2. Upload your design image file as a .dds

    Either directly share your designs with Eugene or Upload your .DDS design into a named folder in the repo under \Vehicles\Textures\Overrides\mini_cooper For example: \Vehicles\Textures\Overrides\mini_cooper\eugenebean\eugenelivery.

3. Ensure that .\Vehicles\Textures\Overrides\mini_cooper\mini_cooper.xml is updated to include a relevant LIVERY OVERRIDE section following the below format:

```
    <LIVERY_OVERRIDE LIVERY="74" NAME="NULL" BASELIVERY="Default">
	  <PREVIEWIMAGE PATH="NULL" />
	  <TEXTURE NAME="BODY" PATH="NULL" />
    </LIVERY_OVERRIDE>
```

Note -  LIVERY number is matched to whatever LIVERY number has been allocated to you and should match the register in this repo's \README.md


## How to update your custom liveries...

I've created a super basic Winforms Powershell script - Figured transparency might be preferable from a security perspective - You can see exactly what the Powershell script is doing if you open it in Notepad.

A summary of it is:

- A pop up application with a default path set for your Automobilista 2 game folder that you may need to amend.

- The installers will verify you've selected the right folder by checking for the Vehicles\Textures\CustomLiveries\Overrides subdirectory being present.

- Then when hitting 'install liveries', this will complete a simple recursive copy from the Repo's 'Vehicles' folder to the aforementioned set game directory.

### To use it:

Download the full repo to your PC.

Right click on **Inky500Installer.ps1** and select 'Run in Powershell'

This should bring up an application that you can choose your Automobilista 2 folder in your SteamApps directory.

Then click 'Install Liveries' to copy the contents of the Vehicles folder in the repo to your game directory.