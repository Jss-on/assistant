import pyperclip
import keyboard
import os
import openai
from datetime import datetime


def copied_words() -> str:
    """
    Waits for the 'ctrl+c' key combination to be pressed and returns the copied text from the clipboard.

    Returns:
        str: The text copied from the clipboard.
    """
    # Define the key combination to detect
    key_combination = "ctrl+c"

    # Wait for the key combination to be pressed
    keyboard.wait(key_combination)

    # Get the text from the clipboard
    selected_text = pyperclip.paste()
    print(selected_text) 

    return selected_text


def get_summary(text) -> str:
    """
    Generates a summary of the given text using OpenAI's GPT-3.5-turbo.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The summary of the text.
    """
    openai.api_key = "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"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Stanford University Mathematics Professor."},
            {
                "role": "user",
                "content": f"Summarize and list all important keypoints. <{text}>",
            },
        ],
    )

    return completion.choices[0].message["content"]


def get_command() -> str:
    """
    Gets a command from the user as input.

    Returns:
        str: The user command.
    """
    return input(":. ")


def get_questions() -> str:
    """
    Gets a list of questions from the user as input.

    Returns:
        str: The user questions.
    """
    return input("Enter your questions: ")


def get_answers(questions: str) -> str:
    """
    Generates answers to the given questions using OpenAI's GPT-3.5-turbo.

    Args:
        questions (str): The questions to be answered.

    Returns:
        str: The answers to the questions.
    """
    openai.api_key = "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"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Respond to the questions as Richard Feynman."},
            {"role": "user", "content": f"{questions}"},
        ],
    )

    return completion.choices[0].message["content"]


def main():
    notes_folder = "Assistant_Notes"
    if not os.path.exists(notes_folder):
        os.makedirs(notes_folder)
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d %H-%M") + ".txt"

    full_path = os.path.join(notes_folder, filename)

    file = open(full_path, "+a", encoding="utf-8")
    file.write("This is a consolidated summary.\n")
    print(f"Created note for this session. Dir: {full_path}")
    while True:
       
        command = get_command()
        # Separate commands for summarizing and questions.
        if command.lower() == ":s":
            text = copied_words()
            proceed = input("Is it the right texts? (y/n): ")
            if proceed.lower() == "y":
                print("Summarizing...")
                summary = get_summary(text)
                file.write(summary)
                file.write("\n\n")
                print(summary)

        elif command.lower() == ":a":
            questions = get_questions()
            file.write("Question:")
            file.write(questions)
            file.write("\n\n")
            
            print("Thinking ...")
            answers = get_answers(questions)
            file.write("Answer:")
            file.write(answers)
            file.write("\n\n")
            print(answers)
        elif command.lower() == ":q":
            break
    file.close()

if __name__ == "__main__":
    main()
