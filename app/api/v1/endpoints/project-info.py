"""
API Routing and Response Formatting
API Endpoints

GET /api/project-info

Returns basic information about the project.

Response (JSON):

json
{
   "name": "GitCollab-Backend",
        "description": "A FastAPI backend service for managing GitHub organization invitations",
        "author": "suraniharsh"
}


"""


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/endpoints/project-info', methods=['GET'])
def project_info():
    """
    GET /endpoints/project-info
    Returns basic project information as JSON:
    - name: Project name
    - description: Short description
    - author: Author's GitHub username
    """
    
    # Project information dictionary
    info = {
        "name": "GitCollab-Backend",
        "description": "A FastAPI backend service for managing GitHub organization invitations",
        "author": "suraniharsh"
    }

    # Return the JSON response with HTTP 200
    return jsonify(info), 200


if __name__ == "__main__":
    app.run(debug=True)
