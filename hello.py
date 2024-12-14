import streamlit as st
from datetime import datetime
import networkx as nx
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle, Event
from uuid import uuid4



# Function to generate a NetworkX graph from session state nodes
def generate_elements(nodes):
    elements = {"nodes": [], "edges": []}

    for node in nodes:
        user_text = f"User: {node['user']['context']}"
        assistant_text = f"Assistant: {node['assistant']['context']}"
        elements['nodes'].append(
            {
                "data": {
                    "id": node["id"],
                    "label": "__node__",
                    "content": [
                        user_text,
                        assistant_text
                    ]
                }
            }
        )

        if node["parent_id"] is not None:
            elements['edges'].append(
                {
                    "data": {
                        "id": str(uuid4()),
                        "label": "FOLLOWS", 
                        "source": node["id"], 
                        "target": node["parent_id"]
                    }
                },
            )

    return elements

# Function to extract chat history based on node_id
def get_chat_history(node_id, nodes, history=None):
    if history is None:
        history = []
    
    # Find the node with the given ID
    current_node = next((node for node in nodes if node["id"] == node_id), None)
    if not current_node:
        return history  # Return if no node is found
    
    # Add assistant and user messages to history
    history.insert(0, {"role": "assistant", "context": current_node["assistant"]["context"]})
    history.insert(0, {"role": "user", "context": current_node["user"]["context"]})
    
    # Recursively traverse to the parent node
    if current_node["parent_id"] is not None:
        return get_chat_history(current_node["parent_id"], nodes, history)
    
    return history

# Function to simulate an AI response (returns a fixed response for now)
def get_assistant_response(user_input):
    return f"Response to: {user_input}"

# Function to add a new message to the nodes
def add_new_message(user_input):
    # Generate timestamps
    current_parent_id =  st.session_state.current_parent_id
    current_time = datetime.now().isoformat()

    # Get assistant's fixed response
    assistant_response = get_assistant_response(user_input)

    # Create a new node
    new_node_id = str(uuid4())
    print(new_node_id)

    new_node = {
        "id": new_node_id,
        "parent_id": current_parent_id,
        "user": {"timestamp": current_time, "context": user_input},
        "assistant": {"timestamp": current_time, "context": assistant_response},
    }
    
    st.session_state.nodes.append(new_node)
    st.session_state.current_parent_id = new_node_id
    st.session_state.history = get_chat_history(new_node_id, st.session_state.nodes)


def my_call_back() -> None:
    val = st.session_state["main_graph"]
    
    if val["action"] == "clicked_node": 
        node_id = val["data"]["target_id"]
        st.session_state.current_parent_id = node_id
        history = get_chat_history(node_id, st.session_state.nodes)
        st.session_state.history = history


layout = "concentric"
# layout = {"name": "concentric", "animate": "end", "nodeDimensionsIncludeLabels": False}


events = [
    Event("clicked_node", "click tap", "node"),
    # Event("another_name", "dblclick dbltap", "*"),
]

# Streamlit app layout
st.set_page_config(layout="wide")
left_column, right_column = st.columns([1, 1])


if 'current_parent_id' not in st.session_state:
    st.session_state.current_parent_id = None  # Start with the last node as the parent


if "nodes" not in st.session_state:
    st.session_state.nodes = [
    {
        "id": "b1e77c5b-d582-4b78-bc2b-f82c54e1b10c",
        "parent_id": None,
        "user": {
            "timestamp": "2024-12-14T10:00:00",
            "context": "Hello, how are you?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:00:05",
            "context": "I'm good, thank you! How can I assist you today?"
        }
    },
    {
        "id": "a3f1b6cf-561e-466d-b29f-876b64b1cfc2",
        "parent_id": "b1e77c5b-d582-4b78-bc2b-f82c54e1b10c",
        "user": {
            "timestamp": "2024-12-14T10:01:00",
            "context": "Can you explain recursion?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:01:10",
            "context": "Sure! Recursion is a function calling itself to solve smaller instances of the same problem."
        }
    },
    {
        "id": "12beac94-4e1d-497d-9a14-21fa4a3e5744",
        "parent_id": "a3f1b6cf-561e-466d-b29f-876b64b1cfc2",
        "user": {
            "timestamp": "2024-12-14T10:02:00",
            "context": "Can you give an example?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:02:10",
            "context": "An example is calculating the factorial of a number using recursion."
        }
    },
    {
        "id": "4ab69f6c-4b8f-4b0e-97c2-291d36c6809d",
        "parent_id": "a3f1b6cf-561e-466d-b29f-876b64b1cfc2",
        "user": {
            "timestamp": "2024-12-14T10:03:00",
            "context": "What are the advantages of recursion?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:03:10",
            "context": "Recursion simplifies code for problems like tree traversal and can break down complex problems into simpler ones."
        }
    },
    {
        "id": "15bc03c9-9572-462f-81c5-6359603fc244",
        "parent_id": "12beac94-4e1d-497d-9a14-21fa4a3e5744",
        "user": {
            "timestamp": "2024-12-14T10:04:00",
            "context": "How does recursion differ from iteration?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:04:10",
            "context": "Recursion uses function calls and stack memory, while iteration uses loops and a constant memory space."
        }
    },
    {
        "id": "c59e76d5-56d4-490b-80b3-68c7a2fa8f35",
        "parent_id": "b1e77c5b-d582-4b78-bc2b-f82c54e1b10c",
        "user": {
            "timestamp": "2024-12-14T10:05:00",
            "context": "What are some common data structures?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:05:10",
            "context": "Some common data structures include arrays, linked lists, stacks, queues, trees, and graphs."
        }
    },
    {
        "id": "cb0e3e8e-6a13-4d2d-986b-399fdf04a7c0",
        "parent_id": "c59e76d5-56d4-490b-80b3-68c7a2fa8f35",
        "user": {
            "timestamp": "2024-12-14T10:06:00",
            "context": "Can you explain stacks and their operations?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:06:10",
            "context": "A stack is a LIFO structure with operations like push, pop, and peek. It's useful for undo functionality and backtracking."
        }
    },
    {
        "id": "8e89cf0d-74f6-4d32-b5cb-9a2c2df70b73",
        "parent_id": "cb0e3e8e-6a13-4d2d-986b-399fdf04a7c0",
        "user": {
            "timestamp": "2024-12-14T10:07:00",
            "context": "Can you provide an example of stack usage?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:07:10",
            "context": "An example is evaluating mathematical expressions using a stack to handle operators and operands."
        }
    },
    {
        "id": "c37d6581-27ea-4f57-b536-3b48663e5188",
        "parent_id": "b1e77c5b-d582-4b78-bc2b-f82c54e1b10c",
        "user": {
            "timestamp": "2024-12-14T10:08:00",
            "context": "What is the difference between an array and a linked list?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:08:10",
            "context": "Arrays have fixed size and contiguous memory, while linked lists use dynamic size and scattered memory with pointers."
        }
    },
    {
        "id": "f45c370e-49db-4f94-bc35-622b2717f4cf",
        "parent_id": "c37d6581-27ea-4f57-b536-3b48663e5188",
        "user": {
            "timestamp": "2024-12-14T10:09:00",
            "context": "When should I use linked lists over arrays?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:09:10",
            "context": "Use linked lists when frequent insertions and deletions are needed, especially in the middle of the structure."
        }
    },
    {
        "id": "289bf2b8-f0c4-4095-bb6d-6dd8f35a54e8",
        "parent_id": "c59e76d5-56d4-490b-80b3-68c7a2fa8f35",
        "user": {
            "timestamp": "2024-12-14T10:10:00",
            "context": "Can you explain tree traversal methods?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:10:10",
            "context": "Tree traversal methods include in-order, pre-order, post-order, and level-order traversal."
        }
    },
    {
        "id": "20c3a183-7b49-4c80-8162-7d672bd5e432",
        "parent_id": "289bf2b8-f0c4-4095-bb6d-6dd8f35a54e8",
        "user": {
            "timestamp": "2024-12-14T10:11:00",
            "context": "What is the difference between pre-order and in-order traversal?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:11:10",
            "context": "Pre-order visits the root first, then left and right subtrees. In-order visits the left subtree, root, then right subtree."
        }
    },
    {
        "id": "d4c89f84-10eb-4d73-9c20-b1f257ee56de",
        "parent_id": "12beac94-4e1d-497d-9a14-21fa4a3e5744",
        "user": {
            "timestamp": "2024-12-14T10:12:00",
            "context": "How is recursion used in solving tree problems?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:12:10",
            "context": "Recursion is used to traverse and solve problems in trees by breaking down tasks into smaller subtrees."
        }
    },
    {
        "id": "c612cbb8-4897-4749-befc-d21c6393b9ef",
        "parent_id": "15bc03c9-9572-462f-81c5-6359603fc244",
        "user": {
            "timestamp": "2024-12-14T10:13:00",
            "context": "Are there any drawbacks to recursion?"
        },
        "assistant": {
            "timestamp": "2024-12-14T10:13:10",
            "context": "Drawbacks include high memory usage due to stack calls and potential stack overflow if not properly managed."
        }
    }
]


if 'history' not in st.session_state:
    st.session_state.history = get_chat_history(st.session_state.current_parent_id, st.session_state.nodes)



# Left Column - Chat Interface
with left_column:
    st.title("AI Chat Interface")
    
    st.markdown("**Current Node ID:** %s" % st.session_state.current_parent_id)

    # Extract chat history from the most recent node
    if st.session_state.nodes:
        chat_history = get_chat_history(st.session_state.current_parent_id, st.session_state.nodes)
    else:
        chat_history = []


    # Display chat messages
    st.markdown("### Chat History")

    with st.container(border=False, height=360):
        for message in chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['context']}")
            elif message["role"] == "assistant":
                st.markdown(f"**Assistant:** {message['context']}")

    # Input field at the bottom
    st.markdown("---")
    user_input = st.text_input("Type your message:", key="chat_input")
    if st.button("Send"):
        if user_input.strip():  # Validate non-empty input
            add_new_message(user_input.strip())  # Add the new message
            st.rerun()

# Right Column - Placeholder for Graph View
with right_column:
    st.title("Graph View")
    
    # Generate elements for st_link_analysis
    elements = generate_elements(st.session_state.nodes)
    
    node_styles = [
        NodeStyle(label="label", color='#FF7F3E', caption="name", icon='person'),
    ]

    edge_styles = [
        EdgeStyle("FOLLOWS", caption='label', directed=True)
    ]

    st_link_analysis(elements, layout, node_styles, edge_styles, events=events, on_change=my_call_back , key="main_graph")