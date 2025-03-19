import argparse
import os
from config import config
from db import init_db
from utils import download_images_from_target

init_db()

def main():
    parser = argparse.ArgumentParser(description="fotosBlog CLI")
    parser.add_argument("-l", "--list", action="store_true", help="List all defined targets")
    parser.add_argument("-t", "--target", help="Target a resource")
    parser.add_argument("-c", "--configure", help="Config a resource")
    parser.add_argument("-o", "--output", help="Setup output destination")
    parser.add_argument("-a", "--all", action="store_true", help="Target all resource")

    args = parser.parse_args()

    if args.output:
        if not args.target:
            print("Error: you need to specify a target")
        elif args.target not in config.endpoints.keys():
            print("Error: target not valid")
        else:
            if not os.path.isdir(args.output):
                print("Error: output has to be a directory")
            else:
                if not os.path.isdir(args.output):
                    print("Error: output directory does not exist")
                    return
                config.output = args.output
                download_images_from_target([args.target])

    elif args.list:
        print(f'Available targets: ')
        for key in config.endpoints.keys():
            print(key, end=" ")
        print()

    elif args.all:
        print('Download images for all targets')
        download_images_from_target(list(config.endpoints.keys()))

    elif args.configure:
        if not args.target:
            print("Error: you need to specify a target")
        elif args.target not in config.endpoints.keys():
            print("Error: target not valid")
        else:
            endpoint = args.configure
            config.endpoints[args.target] = endpoint
            config.save()

    else:
        if args.target not in config.endpoints.keys():
            print("Error: target not valid")
        else:
            print(f'Target selected for {args.target}')
            download_images_from_target([args.target])


if __name__ == "__main__":
    main()
