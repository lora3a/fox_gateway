# Install On RoadRunner

1.  Login inside the RoadRunner

    ```
    ssh acme@<roadrunner ipaddr>
    ```

    !!! info

        ```
        user: acme

        password: acmesystems
        ```

2.  Extend Root Fs

    ```
    sudo extend_rootfs.sh
    ```

3.  Update System

    ```
    sudo apt update && sudo apt upgrade
    ```

4.  Install Dev Package

    ```
    sudo apt install wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev libncurses5-dev libnss3-dev libreadline-dev
    ```

5.  Install Python 3

    ```
    sudo apt install python3 python3-venv python3-pip libpq-dev
    python3 -m pip install --upgrade pip
    python3 -m pip install wheel
    ```

6.  Download fox_gateway project

    === "scp"

        ``` sh title="On PC"
        git clone https://github.com/lora3a/fox_gateway.git
        scp -r fox_gateway/ acme@<roadrunner ipaddr>:~/acme/
        ```

    === "git clone"

        ``` sh title="On RoadRunner"
        sudo apt install git
        git clone https://github.com/lora3a/fox_gateway.git
        ```

7.  Add user to `dialout` group

    ```
    sudo usermod -a -G dialout acme
    ```

8.  install Gateway app

    ```
    cd ~/fox_gateway
    python3 -m pip venv .venv
    . .venv/bin/activate
    python3 -m pip install -r requirements.txt
    python3 -m pip install .
    ```
