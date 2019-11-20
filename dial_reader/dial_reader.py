from application import Application
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('device_name', type=str, help='device name associated with dial, e.g. \'COM3\'')
    args = parser.parse_args()
    app = Application(device_name=args.device_name)
    app.mainloop()
