#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "UrbanMart")
    sys.path.insert(0, project_root)
    os.chdir(project_root)
    from manage import main

    main()
