import os
import dotenv
import gitlab
from code_reviews import get_data

dotenv.load_dotenv(override=True)
TOKEN = os.environ['TOKEN']
gl = gitlab.Gitlab('https://eng-git.canterbury.ac.nz/', private_token=TOKEN)

if __name__ == '__main__':
    project_id = 15303
    project = gl.projects.get(project_id)

    get_data(project)