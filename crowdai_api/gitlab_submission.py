import gitlab
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GitlabSubmission:
    def __init__(self,
                 gitlab_auth_token,
                 project_id,
                 submission_id,
                 challenge_slug,
                 gitlab_url="http://gitlab.crowdai.org"
                ):
        self.gitlab_auth_token = gitlab_auth_token
        self.project_id = project_id
        self.submission_id = submission_id
        self.challenge_slug = challenge_slug
        self.gitlab_url = gitlab_url

        self.gl = gitlab.Gitlab(self.gitlab_url,
                                private_token=self.gitlab_auth_token,
                                ssl_verify=False)

        self.gl.auth()

        # Select relevant project object
        self.project = self.gl.projects.get(self.project_id)
        # print(dir(self.project))
        # print(self.project.members.create{
        #
        # })
        #
        # members = self.project.members.list()
        # member_usernames = [x.username for x in members]
        # print(members, member_usernames)
        # #
        # admin_users = ['Marek_Wydmuch', 'mihahauke']
        # for _idx, _username in enumerate(admin_users):
        #     if _username not in member_usernames:
        #         print("Checking : ", _username)
        #         m = self.gl.users.list(username=_username)
        #         print(m)
                # print("Adding {} as a Master of the repository : ".format(
                #                                                 m.username))
                # print(m.id, m.username)
                # self.project.members.create({
                #                             'user_id': int(m.id),
                #                             'access_level': gitlab.MASTER_ACCESS
        #         #                             })
        # p = self.gl.projects.get(19)
        # u = self.gl.users.get(23)
        # m = p.members.create({'user_id': u.id, 'access_level': gitlab.Group.MASTER_ACCESS})

        issue = self.project.issues.create({'title': 'I have a bug',
                                       'description': 'Something useful here.'})
        print(issue)
