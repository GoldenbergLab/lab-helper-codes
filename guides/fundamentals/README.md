# Fundamentals

Writing code is a necessary part of running modern experiments, and so too are
maintaining and collaborating on written code. While the "fundamentals" of
software (after all, that is the goal of writing code) is a never-ending topic
full of rabbit holes, what follows is a _very_ abridged discussion of those
features most relevant to our lab's coding needs.

<!-- toc -->

- [Command Line](#command-line)
  * [Command Line For Absolute Beginners](#command-line-for-absolute-beginners)
  * [Command Line After Some Practice](#command-line-after-some-practice)
- [Text Editors](#text-editors)
  * [Editors Available](#editors-available)
  * [Editor Configurations](#editor-configurations)

<!-- tocstop -->

## Command Line

The _command line_ is the best way to interact with computers and that is its
sole function. Everything you do with a command line is fundamentally about sending
commands that a computer interprets and tries to respond to.

### Command Line For Absolute Beginners

If you have never used the command line, this section is for you.

**Is the command line hard to use?** If you've never learned how to use it, yes. But
that just means it is probably time to learn; **everyone** can learn how to use the command
line, and that includes **you**!

**Where should I start?** Start with [Terminus](http://web.mit.edu/mprat/Public/web/Terminus/Web/main.html),
a game created by MIT computer scientists to help you learn command line basics.

### Command Line After Some Practice

Once you feel more comfortable with the concept of command line tools, and have had some
real experience using one for a project, it's time to step up your game. While many
avenues are available, these referenced links include useful collections of materials
to make your command line experience even better:

- [The Art of Command Line](https://github.com/jlevy/the-art-of-command-line)
- [MacOS Command Line](https://github.com/herrbischoff/awesome-macos-command-line)

## Text Editors

_Text editors_ are the software applications we use to read and write file contents.
In most cases, this means writing programs with code, so we can run studies online or
analyze data to verify results.

### Editors Available

There are a variety of text editors available. Some of the most popular editors that
are used by software developers at every skill level include:

- Shell
  - [Vim](https://www.vim.org/)
  - [Emacs](https://www.gnu.org/software/emacs/)
- Applications
  - [Atom](https://atom.io/)
  - [Sublime Text](https://www.sublimetext.com/)
  - [VisualStudio Code](https://code.visualstudio.com/)

Regardless of which you pick, do some research to learn about the different editors.
Ultimately it is up to you to choose the editor that works best for you (i.e., one
may have a color scheme and comes with keyboard shortcuts that you really like, while
another may have great autocompletion packages and a nice project files search feature).

### Editor Configurations

Working on teams with distributed version control (Git) requires us to make
sure that our _text editing environments_ are compatible with one another.

**What is a text editing environment?** The settings configured for your text editor
that define how your text is written, like character sets, indent spacing, etc.

To make compatible configuration easy, opt for using a shared configuration that everyone
uses on the team. Use https://editorconfig.org/.
