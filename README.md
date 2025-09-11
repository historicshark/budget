# budget program

## How to download

Go to [releases](https://github.com/historicshark/budget/releases).

![step1](docs/step1.png)

I have a Windows version and a Mac ARM version of the program that can be downloaded.

![step2](docs/step2.png)

Download the zip file. If you are on Windows, it will work best if you extract the zip file in your Documents folder. On Mac, extracting in your home folder will work best. After extracting, there should be a `budget_program` folder containing the executable `budget_program` and a folder called `_internal`, which contains files needed for the program. Now you can double-click the executable and run it to start the program.

## How to use
To import transactions from your bank, download your statement as a .ofx, Quickbooks .qbo, Quicken .qfx, or other .ofx - like file. Currently .csv files are not able to be imported.

Next, click the "import" button in the program, and select the downloaded file on your computer. From there, you will categorize each transaction in the statement. The program will try to guess which category each transaction should belong to based on the "Location" and a list of **keyword**:**category** rules. If a **keyword** appears in the "Location" of the transaction, the program will guess the corresponding **category**. If you choose a different category than the one that was guessed, the program will ask if you want to add a new **keyword**:**category** rule. The text you enter as the new rule will be the **keyword**, and the category you chose will be the **category**. If you leave the text unchanged, all future transactions exactly matching the current one's "Location" will be guessed to be the same category.

If you want to skip a transaction such as payments or transfers between accounts, you can press the skip button. 

Along the bottom of the window is a bar showing keyboard shortcuts that are available to make using the program faster.
