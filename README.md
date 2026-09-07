# eBiblio

This is a simple SPA (Single Page Application) for the management of a home library. It has support for full search of all attributes, genre handling, checking books out and more. It is intentionally designed to be very lightweight and simple, and does not support users, or general library management tools.

## Installation

1. Clone the git repo, and update [compose.yml](./compose.yml) with your environment variables, and correct port number.

2. Run `docker compose build -d`

3. When that finishes, run `docker compose up -d`.

Then you can navigate to the port number on localhost and begin using it.

## Configuration

There are a few variables that should be configured before use, by editing [config.toml](./config.toml). You will probably want to configure primary color, and default book owner to something that you like, but that is not necessary.

## Usage

In eBiblio, books are sorted by genre, then further distinguished by subject, author, and owner. So to start you will want to add the genres you would like to categorize by. There are some already pre added, but you will probably want more.

To add some more genres, you will want to first define some genres in [config.toml](./config.toml). Just make sure not to duplicate an entry.

After adding genres then restart the aplication with `docker compose down` and `docker compose up -d`.

Once you have defined the Genres you would like, you can then add some books. In the bottom bar, input the required information. All entries are required except for `Notes`. In order to make searching for books easier, add a comma seperated list of as many subjects you think the book touches, then you can head to the `Search` tab, and preface your search with `subject: ` and search directly for those subjects.

### Checking Out

Once you have inputted books, if you would like to remove a book from the shelf and read it, you can check it out by clicking the checkmark icon. You can return it by tapping the same icon, and a list of checked out books can be found in the `Checked Out` tab.

## Stack

eBiblio is built with sqlite, NiceGui, Tortoise-Orm, and Docker.
