# Fundamentals

Writing code is a necessary part of running modern experiments, and so too are
maintaining and collaborating on written code. While the "fundamentals" of
software (after all, that is the goal of writing code) is a never-ending topic
full of rabbit holes, what follows is a _very_ abridged discussion of those
features most relevant to our lab's coding needs.

<!-- toc -->

- [Text Editors](#text-editors)
  * [Editors Available](#editors-available)
  * [Editor Configurations](#editor-configurations)

<!-- tocstop -->

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
