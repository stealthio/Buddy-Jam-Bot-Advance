# Buddy-Jam-Bot (Advance) [![buddyjam]](https://www.reddit.com/r/BuddyJam/) [![discord]](https://discord.gg/V2SaHEM)

<img src="https://raw.githubusercontent.com/stealthio/Buddy-Jam-Bot-Advance/master/img/logo.png?token=AEZSBNXC3D7BTG6DBOXP2JS5HKR2O" align="right"
     title="BuddyJam Logo" width="120" height="120">

This is the second version of the **Buddy-Jam-Bot**, it's still WIP and it's main purpose is automatizing most manual
processes of the Buddy-Jam staff. Which is includes:

 * Announcements
 * Votings
 * User-Interaction
 * A score system to reward interaction

[buddyjam]: https://img.shields.io/badge/-Buddy--Jam-red.svg
[discord]: https://img.shields.io/badge/-Discord-blue.svg

## Commands

### `announcejam`

Posts an announcement that the next jam is about to start and starts a voting for the next theme of the next jam. It also
includes an automatically generated link to the itch.io page for the next jam.

### `startjam`

Posts an announcement that the next jam has officially started - for the theme of the jam it will take the message
with most :thumbsup: reactions in the voting channel and wipes the voting channel clean.

### `suggest`

Adds a theme to the current theme voting pool

### `setjamno`

Sets the number for the current Buddy-Jam. It is used to generate the Itch.io/Crowdforge links.

### `buddyscore`

Tells the user his/her current Buddy-Score which is gained by submitting games and several user interactions.

### `hello`

Answers with a hello message, mainly used to test if the bot is currently active.

### `wipechannels`

This command clears every channel of the server. It is only implemented for testing purposes!