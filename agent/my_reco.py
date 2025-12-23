from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context


@AgentServer.custom_recognition("sign_in_reward_collect")
class MyRecongition(CustomRecognition):

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        
        for y in range (593, 593-73*4-1, -73):
            for x in range (900, 900-78*5-1, -78):
                result = context.run_recognition(
                    "CheckSignInRewardBox",
                    argv.image,
                    pipeline_override = {
                        "CheckSignInRewardBox": {
                            "recognition": "ColorMatch", 
                            "roi": [x, y, 3, 3], 
                            "lower": [188, 188, 188],
                            "upper": [196, 196, 196],
                        }
                    },
                )
                print("Checking position:", x, y, "Result:", result.hit)
                if result.hit:
                #     context.run_action(
                #         "RobustClick",
                #         result.box,
                #         result.best_result.detail,
                #         pipeline_override = {
                #             "RobustClick": {
                #                 "action": "LongPress", 
                #                 "duration": 300, 
                #             }
                #         },
                #     )
                    return CustomRecognition.AnalyzeResult(
                        box=(x, y, 1, 1), detail="Task Complete"
                    )

        return CustomRecognition.AnalyzeResult(
            box=(0, 0, 0, 0), detail="Task Failed"
        )
