# init_project.ps1 - Project structure creator
# Author: Victor Kulichenko

Write-Host "Creating ORBITA PRIME structure..." -ForegroundColor Cyan

function New-DjangoApp {
    param([string]$Name)
    Write-Host "App: $Name" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "$Name","$Name\tests","$Name\migrations" -Force | Out-Null
    New-Item -ItemType File -Path @(
        "$Name\__init__.py","$Name\apps.py","$Name\models.py","$Name\managers.py",
        "$Name\forms.py","$Name\services.py","$Name\selectors.py","$Name\views.py",
        "$Name\urls.py","$Name\admin.py","$Name\tests\__init__.py","$Name\migrations\__init__.py"
    ) -Force | Out-Null
}

# Root files
New-Item -ItemType File -Path manage.py,requirements.txt,README.md,.gitignore,.env.example,pyproject.toml,pytest.ini -Force

# Config
New-Item -ItemType Directory -Path config -Force
New-Item -ItemType File -Path config\__init__.py,config\settings.py,config\urls.py,config\wsgi.py,config\asgi.py -Force

# Apps
New-DjangoApp -Name "accounts"
New-DjangoApp -Name "cart"

# Extra files
New-Item -ItemType File -Path accounts\validators.py,accounts\tokens.py,accounts\utils.py -Force
New-Item -ItemType File -Path accounts\tests\test_models.py,accounts\tests\test_views.py,accounts\tests\test_security.py -Force
New-Item -ItemType File -Path cart\utils.py,cart\session.py,cart\tests\test_utils.py -Force

# Templates
New-Item -ItemType Directory -Path templates,templates\accounts,templates\cart,templates\legal -Force
New-Item -ItemType File -Path templates\base.html,templates\home.html -Force
New-Item -ItemType File -Path templates\accounts\register.html,templates\accounts\login.html,templates\accounts\profile.html,templates\accounts\password_reset.html,templates\accounts\delete_account.html -Force
New-Item -ItemType File -Path templates\cart\cart.html -Force
New-Item -ItemType File -Path templates\legal\privacy_policy.html,templates\legal\user_agreement.html -Force

# Static
New-Item -ItemType Directory -Path static\css,static\js,static\images -Force
New-Item -ItemType File -Path static\css\space-theme.css,static\js\cart.js,static\images\logo.svg -Force

# Media
New-Item -ItemType Directory -Path media\products,media\avatars -Force

Write-Host "Done!" -ForegroundColor Green
Write-Host "Files:" -ForegroundColor Cyan
(Get-ChildItem -Recurse -File).Count