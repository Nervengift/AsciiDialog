Asciidialog
===========

    //========================================\\
    |   _     _ _______                _____   |
    |   |_____| |______ |      |      |     |  |
    |   |     | |______ |_____ |_____ |_____|  |
    |                                          |
    \\========================================//

Asciidialog shows a ncurses message. It can be colored and figletified (figlet should be installed to do so ;) )

Usage
-----

    asciidialog foo

Shows a simple dialog saying "foo".

    asciidialog -f -a "-t -f cyberlarge" foo

Beautify the text with figlet. Additionally arguments to figlet can be given via the *-a* argument (defaults to "-t"(use terminal's full width)).

    asciidialog -c red ACCESS DENIED

The *-c* option colors the output. Can be "red", "blue", "green", "white" and "default" (don't change).
