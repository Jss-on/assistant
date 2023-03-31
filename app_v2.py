import os
import pyperclip
import keyboard
import openai
from datetime import datetime

def copied_words(prev_texts) -> str:

    while True:
    
        key_combination = "ctrl+c"
        keyboard.wait(key_combination)
        selected_text = pyperclip.paste()
        if prev_texts != selected_text:
            print("Copied")
            break
        else:
            print("Try again")

    # print(selected_text)
    return selected_text

def call_openai_api(prompt) -> str:
    openai.api_key = 'Your OPENAI API key here'

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
    )
    return completion.choices[0].message["content"]

def get_summary(text) -> str:
    prompt = {
        "system": "Stanford University Mathematics Professor.",
        "user": f"Summarize and list all important keypoints. <{text}>",
    }
    return call_openai_api(prompt)

def get_answers(questions: str) -> str:
    prompt = {
        "system": "Respond to the questions as Richard Feynman.",
        "user": f"{questions}",
    }
    return call_openai_api(prompt)

def get_command() -> str:
    return input("Enter command (s: summarize, a: ask, q: quit): ")

def get_questions() -> str:
    return input("Enter your questions: ")

def main():
    notes_folder = "Assistant_Notes"
    if not os.path.exists(notes_folder):
        os.makedirs(notes_folder)
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d %H-%M") + ".txt"

    full_path = os.path.join(notes_folder, filename)
    prev_texts = ""
    with open(full_path, "a", encoding="utf-8") as file:
        file.write("This is a consolidated summary.\n")
        print(f"Created note for this session. Dir: {full_path}")
        while True:
            command = get_command().lower()
            if command == "s":
                text = copied_words(prev_texts)
                prev_texts = text[:]
                # proceed = input("Is it the right texts? (y/n): ").lower()
                # if proceed == "y":
                print("Summarizing...")
                summary = get_summary(text)
                file.write(summary)
                file.write("\n\n")
                print(summary)
            elif command == "a":
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
            elif command == "q":
                break

if __name__ == "__main__":
   main()
