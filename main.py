

class Branch:
    name = ""
    commits = []

    def __init__(self, name):
        self.name = name
        self.commits = []

    def get_name(self):
        return self.name

    def get_commits(self):
        return self.commits

    def add_commit(self, commit):
        self.commits.append(commit)


class Commit:
    type = ""

    branch_from = ""
    merge_from = ""

    message = ""
    commit_id = ""
    last_commit_id = ""

    def __init__(self, commit_id, message):
        self.type = "init"
        self.commit_id = commit_id
        self.message = message

    def __init__(self, commit_id, message, last_commit_id):
        self.type = "commit"
        self.commit_id = commit_id
        self.message = message
        self.last_commit_id = last_commit_id

    def __init__(self, commit_id, message, last_commit_id, branch_from):
        self.type = "newbranch"
        self.commit_id = commit_id
        self.message = message
        self.last_commit_id = last_commit_id
        self.branch_from = branch_from

    def __init__(self, commit_id, message, last_commit_id, merge_from, merge):
        self.type = "newbranch"
        self.commit_id = commit_id
        self.message = message
        self.last_commit_id = last_commit_id
        self.merge_from = merge_from

    def get_type(self):
        return self.type

    def get_branch_from(self):
        return self.branch_from

    def get_merge_from(self):
        return self.merge_from

    def get_message(self):
        return self.message

    def get_commit_id(self):
        return self.commit_id

    def get_last_commit_id(self):
        return self.last_commit_id

    def __str__(self):
        return f'Commit №{self.commit_id}' \
               f'\nType: {self.type}' \
               f'\nLast commit id: {self.last_commit_id}' \
               f'\nMessage: {self.message}' \
               f'\nBranch from (if exists): {self.branch_from}' \
               f'\nMerge from (if exists): {self.merge_from}'


class GitDataProcess:
    branches = []

    def __init__(self):
        self.branches = []

    def add_branch(self, branch):
        self.branches.append(branch)

    def get_message_from_branch(self, commit_id, branch_name):
        for branch in self.branches:
            if branch.get_name() == branch_name:
                for commit in branch.get_commits():
                    if commit.get_commit_id() == commit_id:
                        return commit.get_message()
        print(f'Message (branch: {branch_name}, commit id: {commit_id}) not found')
        return "error"

    def make_tree(self, path):
        tb = TreeBuilder(path)

        for branch in self.branches:
            for commit in branch.get_commits():
                if commit.get_type() == "init":
                    pass
                elif commit.get_type() == "commit":
                    last_commit = None
                    for branch_c in self.branches:
                        for commit_c in branch_c.get_commits():
                            if commit_c.get_commit_id() == commit.get_last_commit_id():
                                last_commit = commit_c
                    


class Node:
    parent = None
    children = []
    data = None

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.add_child(self)

    def get_data(self):
        return self.data

    def add_child(self, child):
        self.children.append(child)

    def show(self, level=0):
        print("\t" * level + str(self.data))
        for child in self.children:
            child.show(level+1)


class TreeBuilder:
    path = ""
    nodes = []

    def __init__(self, path):
        self.path = path
        self.nodes = []

    def add_node(self, parent, new):
        temp = [parent, new]
        self.nodes.append(temp)

    def save_tree(self):
        with open(self.path, "w", encoding="utf-8") as output:
            output.write("digraph G {\n")
            for node in self.nodes:
                temp = ""
                temp += node[0].get_data().get_commit_id()
                temp += node[0].get_data().get_message()

                temp += " -> "
                temp += node[1].get_data().get_commit_id()
                temp += node[1].get_data().get_message()

                output.write(temp + "\n")
            output.write("}")


if __name__ == "__main__":
    test_path = ""  # enter path to repository here
    path_commits = test_path.replace("\\", "/") + ".git/logs/refs/heads"

    process = GitDataProcess()

    test_node1 = Node("123")
    test_node2 = Node("1234", test_node1)
    test_node3 = Node("12345", test_node2)
    test_node4 = Node("123456", test_node1)
    test_node5 = Node("1234567", test_node3)
    test_node1.show()