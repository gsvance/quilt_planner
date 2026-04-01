#!/usr/bin/env python3

from interface import Interface


def main():
    interface = Interface()
    interface.run_click_loop()
    interface.finish()


if __name__ == "__main__":
    main()
