import sys
import controlnet_sd15_train
import create_control
from .functionDir import named, promptcreate

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <function-name> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'controlnet_train':
        controlnet_sd15_train.main()  # 假设这是 controlnet_sd15_train.py 中的主函数
    elif command == 'create_control':
        create_control.main()  # 假设这是 create_control.py 中的主函数
    elif command == 'named':
        named.main()  # 假设这是 named.py 中的主函数
    elif command == 'promptcreate':
        promptcreate.main()  # 假设这是 promptcreate.py 中的主函数
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()