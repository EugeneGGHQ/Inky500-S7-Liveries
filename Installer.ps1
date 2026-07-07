Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- CONFIG ---
$RequiredSubDir = "Vehicles\Textures\CustomLiveries\Overrides"
$DefaultPath = "C:\Program Files (x86)\Steam\steamapps\common\Automobilista 2"

# Source folder: ALWAYS the "Vehicles" folder next to the installer script
$ScriptRoot = Split-Path -Parent $PSCommandPath
$SourceFolder = Join-Path $ScriptRoot "Vehicles"

# --- FORM SETUP ---

$form = New-Object System.Windows.Forms.Form
$form.Text = "Automobilista 2 Livery Installer"
$form.Size = New-Object System.Drawing.Size(600,260)
$form.StartPosition = "CenterScreen"

# --- CUSTOM ICON ---
$IconPath = Join-Path $ScriptRoot "gghq.ico"
$form.Icon = New-Object System.Drawing.Icon($IconPath)

# --- UI ELEMENTS ---

$label = New-Object System.Windows.Forms.Label
$label.Text = "Select your Automobilista 2 installation directory:"
$label.Location = New-Object System.Drawing.Point(10,20)
$label.Size = New-Object System.Drawing.Size(560,20)
$form.Controls.Add($label)

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Location = New-Object System.Drawing.Point(10,50)
$textBox.Size = New-Object System.Drawing.Size(450,20)
$textBox.Text = $DefaultPath
$form.Controls.Add($textBox)

$browseButton = New-Object System.Windows.Forms.Button
$browseButton.Text = "Browse"
$browseButton.Location = New-Object System.Drawing.Point(470,48)
$browseButton.Size = New-Object System.Drawing.Size(100,25)
$form.Controls.Add($browseButton)

$folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog

$browseButton.Add_Click({
    if ($folderDialog.ShowDialog() -eq "OK") {
        $textBox.Text = $folderDialog.SelectedPath
    }
})

# --- PROGRESS BAR ---
$progressBar = New-Object System.Windows.Forms.ProgressBar
$progressBar.Location = New-Object System.Drawing.Point(10,140)
$progressBar.Size = New-Object System.Drawing.Size(560,25)
$progressBar.Style = "Continuous"
$form.Controls.Add($progressBar)

# --- INSTALL BUTTON ---
$installButton = New-Object System.Windows.Forms.Button
$installButton.Text = "Install Liveries"
$installButton.Location = New-Object System.Drawing.Point(10,100)
$installButton.Size = New-Object System.Drawing.Size(560,40)
$form.Controls.Add($installButton)

# --- VALIDATION + COPY LOGIC ---
$installButton.Add_Click({
    $gamePath = $textBox.Text
    $targetSubDir = Join-Path $gamePath $RequiredSubDir

    if (-not (Test-Path $targetSubDir)) {
        [System.Windows.Forms.MessageBox]::Show(
            "The selected directory does not contain:`n$RequiredSubDir",
            "Invalid Directory",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        return
    }

    if (-not (Test-Path $SourceFolder)) {
        [System.Windows.Forms.MessageBox]::Show(
            "Installer error: Source folder not found:`n$SourceFolder",
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        return
    }

    # Count files for progress bar
    $files = Get-ChildItem -Path $SourceFolder -Recurse -File
    $total = $files.Count
    $progressBar.Maximum = $total
    $progressBar.Value = 0

    try {
        foreach ($file in $files) {
            # Determine destination path
            $relative = $file.FullName.Substring($SourceFolder.Length)
            $dest = Join-Path $gamePath $relative

            # Ensure directory exists
            $destDir = Split-Path $dest -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir | Out-Null
            }

            # Copy file
            Copy-Item $file.FullName $dest -Force

            # Update progress bar
            $progressBar.Value++
            $form.Refresh()
        }

        [System.Windows.Forms.MessageBox]::Show(
            "Liveries installed successfully.`n`nRestart Automobilista 2 if it is currently running.",
            "Installation Complete",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Information
        )
    }
    catch {
        [System.Windows.Forms.MessageBox]::Show(
            "Installation failed:`n$($_.Exception.Message)",
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
    }
})

# --- RUN FORM ---
[void]$form.ShowDialog()
