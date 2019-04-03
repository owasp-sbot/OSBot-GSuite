import unittest
from time import sleep
from unittest import TestCase

from pbx_gs_python_utils.utils.Assert        import Assert
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.aws.CodeBuild import CodeBuild
from pbx_gs_python_utils.utils.aws.IAM       import IAM


class Create_Code_Build:

    def __init__(self):
        self.account_id         = '244560807427'                                # move to config value or AWS Secret
        self.project_name       = 'gsbot-gsuite'
        self.project_repo       = 'https://github.com/pbx-gs/{0}'.format(self.project_name)
        self.service_role       = 'arn:aws:iam::{0}:role/{1}'                  .format(self.account_id, self.project_name)
        self.project_arn        = 'arn:aws:codebuild:eu-west-2:{0}:project/{1}'.format(self.account_id, self.project_name     )
        self.assume_policy      = {'Statement': [{'Action'   : 'sts:AssumeRole'                     ,
                                                  'Effect'   : 'Allow'                              ,
                                                  'Principal': {'Service': 'codebuild.amazonaws.com'}}]}

        self.code_build = CodeBuild(role_name=self.project_name, project_name=self.project_name)
        self.iam        = IAM      (role_name=self.project_name                                )

    def setup(self,delete_on_setup=False):
        if delete_on_setup:
            self.code_build.project_delete()
            self.iam.role_delete()
        if self.code_build.project_exists() is False:
            assert self.code_build.project_exists() is False
            self.iam.role_create(self.assume_policy)                     # create role
            assert self.iam.role_info().get('Arn') == self.service_role  # confirm the role exists
            sleep(1)
            self.code_build.project_create(self.project_repo,
                                           self.service_role)            #  in a non-deterministic way, this sometimes throws the error: CodeBuild is not authorized to perform: sts:AssumeRole

    def teardown(self, delete_on_teardown=False):

        assert self.code_build.project_exists() is True
        assert self.iam.role_exists() is True
        if delete_on_teardown:
            self.code_build.project_delete()
            self.iam.role_delete()
            assert self.code_build.project_exists() is False
            assert self.iam.role_exists() is False

    def create_policies(self):
        cloud_watch_arn = "arn:aws:logs:eu-west-2:244560807427:log-group:/aws/codebuild/{0}:log-stream:*".format(self.project_name)
        policies = {"Cloud-Watch-Policy": { "Version": "2012-10-17",
                                            "Statement": [{   "Sid": "GsBotPolicy",
                                                              "Effect": "Allow",
                                                              "Action": [ "logs:CreateLogGroup"  ,
                                                                          "logs:CreateLogStream" ,
                                                                          "logs:PutLogEvents"   ],
                                                              "Resource": [ cloud_watch_arn ]}]},
                    "Secret-Manager": {
                                            "Version"  : "2012-10-17",
                                            "Statement": [{   "Sid"    : "GsBotPolicy",
                                                              "Effect" : "Allow",
                                                              "Action" : [ "secretsmanager:GetSecretValue","secretsmanager:DescribeSecret"],
                                                              "Resource": ["arn:aws:secretsmanager:eu-west-2:244560807427:secret:slack-gs-bot-*",
                                                                           "arn:aws:secretsmanager:eu-west-2:244560807427:secret:elastic_gsuite_data-*"]}]},
                    "Download_Image": {     "Version": "2012-10-17",
                                            "Statement": [{   "Effect": "Allow",
                                                              "Principal": {
                                                                  "AWS": "arn:aws:iam::244560807427:root"
                                                              },
                                                              "Action": [   "ecr:GetAuthorizationToken",
                                                                            "ecr:BatchCheckLayerAvailability",
                                                                            "ecr:GetDownloadUrlForLayer",
                                                                            "ecr:GetRepositoryPolicy",
                                                                            "ecr:DescribeRepositories",
                                                                            "ecr:ListImages",
                                                                            "ecr:DescribeImages",
                                                                            "ecr:BatchGetImage"],
                                                              "Resource": "*"}]}}

        policies_arns  = list(self.code_build.iam.role_policies().values())
        policies_names = list(self.code_build.iam.role_policies().keys())
        self.code_build.iam.role_policies_detach(policies_arns)
        for policies_name in policies_names:
            self.code_build.iam.policy_delete(policies_name)

        self.code_build.policies_create(policies)


class test_Create_Code_Build(TestCase):

    @classmethod
    def setUpClass(cls):
        Create_Code_Build().setup(delete_on_setup=False)

    @classmethod
    def tearDownClass(cls):
        Create_Code_Build().teardown(delete_on_teardown = False)

    def setUp(self):
        self.api = Create_Code_Build()

    def test__init__(self):
        Assert(self.api.project_name).is_equal('gsbot-gsuite'                          )      # confirm init vars setup
        Assert(self.api.project_repo).is_equal('https://github.com/pbx-gs/gsbot-gsuite')
        assert 'gsbot-gsuite' in self.api.code_build.projects()                               # confirm project has been created
        assert self.api.iam.role_exists() is True                                             # confirm role has been created

    def test_create_policies(self):
        self.api.create_policies()

    def test_build_start(self):
        build_id = self.api.code_build.build_start()
        result = self.api.code_build.build_wait_for_completion(build_id, max_attempts=100, log_status=True)
        Dev.pprint(result)
    # use cases

    def test_create_policies_and_trigger_build(self):
        self.api.create_policies()
        build_id = self.api.code_build.build_start()
        result = self.api.code_build.build_wait_for_completion(build_id,max_attempts=100,log_status=True)
        Dev.pprint(result)
        #Dev.pprint(result.get('phases')[2].get('contexts')[0].get('message') )

