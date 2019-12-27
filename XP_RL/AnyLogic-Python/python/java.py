"""
test to get java output in a python program
"""

# import
import json
import pickle
import re
import subprocess


def compile_java(java_file):
    """
    Compile Java file.
    Not needed.
    """
    subprocess.check_call(['javac', java_file])
    return


def execute_java(java_cmd, q):
    """
    run java file.
    """
    proc = subprocess.Popen(
        java_cmd, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, stderr = proc.communicate(q)
    return stdout.decode("utf-8")


def extract_elements(output):
    """
    extract states, actions and returns
    """
    # get data
    matched = re.findall(r".*?\[(.*)].*", output)
    # states
    states_text = re.findall(r'[+-]?\d+(?:\.\d+)?', matched[0])
    states = []
    ind = 0
    s = [[0, 0], [0, 0]]
    for i in states_text:
        if ind > 1:
            s[1][ind - 2] = int(i)
        else:
            s[0][ind] = int(i)
        if (ind + 1) % 4 == 0:
            # check if it's Delta
            if s[1][0] < 0 or s[1][0] > 7 or\
               s[1][1] < 0 or s[1][1] > 7:
                states.append('Delta')
            else:
                states.append(
                    (tuple(s[0]), tuple(s[1]))
                )
            s = [[0, 0], [0, 0]]
            ind = 0
            continue
        ind += 1
    # actions
    actions = []
    for i in matched[1]:
        if i != ' ' and i != ',':
            actions.append(i)
    # returns
    returns_text = re.findall(r'[+-]?\d+(?:\.\d+)?', matched[2])
    returns = [
        float(i)
        for i in returns_text
    ]
    return states, actions, returns


def prepare_q(q):
    """
    prepare q values to transfer to java.
    """
    q_str = {}
    for key in q.keys():
        if key[0] == 'Delta':
            s = 'Delta-{}'.format(
                key[1]
            )
        else:
            s = '{}-{}-{}-{}-{}'.format(
                key[0][0][0], key[0][0][1], key[0][1][0],
                key[0][1][1], key[1]
            )
        q_str[s] = q[key]
    byte_q = json.dumps(q_str).encode('utf-8')
    return byte_q


def main():
    """
    main
    """
    q = pickle.load(open('q.pickle', 'rb'))
    byte_q = prepare_q(q)
    # print(byte_q)
    # return
    java_cmd = [
        '/Library/Java/JavaVirtualMachines/openjdk-13.0.1.jdk'
        '/Contents/Home/bin/java',
        '-Dfile.encoding=UTF-8',
        '@/var/folders/64/557sfr5j0bggvbv05_vnrp8w0000gn/T'
        '/cp_4e1r4bmo1vzn71trijsjwm6r5.argfile',
        'p.App'
    ]
    output = execute_java('java/Test.java', java_cmd, byte_q)
    print(output)
    states, actions, returns = extract_elements(output)
    return


if __name__ == "__main__":
    main()
