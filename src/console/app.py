import config
import sys
from definitions import (
    read_csv_and_add_content_to_tuple,
    join_tuple,
    remove_duplicates_from_list,
    convert_list_to_table,
    is_empty_csv,
    input_url_or_id,
    is_string_valid_url,
    add_id_to_csv,
    want_another_video_added,
    count_items_in_table,
    want_playlist_deleted,
    reset_playlist,
    is_string_valid_youtube_url,
    cut_url_to_id,
    delete_items_from_playlist,
    create_comma_seperated_string,
    add_title_to_playlist,
    generate_video_ids_url,
    generate_playlist_url,
    output_generated_playlist_url,
    open_playlist_url_in_webbrowser,
)
from os import system, name


def clear():
    _ = system("cls") if name == "nt" else system("clear")


def welcome_message():
    clear()
    print("-" * 62)
    print("Welcome to the YouTube Playlist Generator by Christian Hofmann")
    print("-" * 62)


def main_menu():
    print("[0] to view current playlist")
    print("[1] to create a new playlist")
    print("[2] to add videos to the playlist")
    print("[3] to delete certain videos from the playlist")
    print("[4] to generate the URL for the playlist")
    print("[5] to exit the program")

    choice = input("\nPlease select an option: ")
    if choice == "0":
        option_zero()
    elif choice == "1":
        option_one()
    elif choice == "2":
        option_two()
    elif choice == "3":
        option_three()
    elif choice == "4":
        option_four()
    elif choice == "5":
        option_five()
    else:
        print(
            "\nInvalid option. Please enter a number between [0] and [4]. Or press [5] to exit the program.\n"
        )
        main_menu()


def option_zero():
    clear()
    tuple = read_csv_and_add_content_to_tuple()
    list = join_tuple(tuple)
    list_without_duplicates = remove_duplicates_from_list(list)

    list_with_video_ids = convert_list_to_table(list_without_duplicates)

    if list:
        print(
            f"\nThese video ids are currently in your playlist: {list_with_video_ids}\n"
        )
        print(f"sum of video ids: {count_items_in_table(list_with_video_ids)}\n")
    else:
        print("There are no videos in your playlist yet.\n")
    main_menu()


def option_one():
    clear()
    if is_empty_csv("video_ids.csv"):
        print("\nYour playlist is already empty!\n")
    elif want_playlist_deleted():
        reset_playlist()
    else:
        print("\nYou didn't choose to create a new playlist.\n")
    main_menu()


def option_two():
    clear()
    input = input_url_or_id()
    if is_string_valid_url(input) and is_string_valid_youtube_url(
        input
    ):  # if input is a valid YouTube URL
        id = cut_url_to_id(input)
    else:
        id = input
    add_id_to_csv(id)
    print(f"\nVideo '{id}' was successfully added to the playlist.\n")
    if want_another_video_added():
        option_two()
    main_menu()


def option_three():
    clear()
    tuple = read_csv_and_add_content_to_tuple()
    list = join_tuple(tuple)
    list_without_duplicates = remove_duplicates_from_list(list)

    print(
        f"\nThese video ids are currently in your playlist: {convert_list_to_table(list_without_duplicates)}\n"
    )
    delete_items_from_playlist(list_without_duplicates)
    main_menu()


def option_four():
    clear()
    if not is_empty_csv("video_ids.csv"):
        tuple = read_csv_and_add_content_to_tuple()
        list = join_tuple(tuple)
        comma_seperated_string = create_comma_seperated_string(list)
        playlist_title = config.youtube_playlist_title
        add_title_to_playlist(playlist_title)

        generate_video_ids_url(comma_seperated_string)
        if generate_playlist_url(config.youtube_generated_video_ids_url):
            output_generated_playlist_url()
            open_playlist_url_in_webbrowser()
    else:
        print(
            "\nYour playlist is empty! Add at least two videos in order to generate a playlist URL.\n"
        )
    main_menu()


def option_five():
    sys.exit(0)


def main():
    if config.first_start == True:
        welcome_message()
        config.first_start = False
    main_menu()


if __name__ == "__main__":
    main()