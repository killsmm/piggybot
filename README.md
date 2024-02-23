# Gnerate one file executable
```
    pyinstaller piggybot.spec
```

# Deploy
+ copy dist/main to the production machine
+ run the executable

# Deploy issue
## ssl related issue when run the executable
Install the python3-certifi in the production machine which is running ubuntu
```
    sudo apt install python3-certifi
```