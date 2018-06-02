from naoqi import ALProxy
import time

IP = "192.168.1.120"
port = 9559

manager_proxy = ALProxy("ALBehaviorManager", IP, port)
names = manager_proxy.getInstalledBehaviors()
#print(names)

behavior_name = "canavanplacemusic-16a6c1/CanavanPlace music"

if (manager_proxy.isBehaviorInstalled(behavior_name)):
    print("installed")
    if (not manager_proxy.isBehaviorRunning(behavior_name)):
        manager_proxy.post.runBehavior(behavior_name)
        time.sleep(0.5)
    else:
        print("Behavior is already running.")
        manager_proxy.stopBehavior(behavior_name)
else:
    print("Behavior not found")
