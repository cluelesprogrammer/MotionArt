from body import Body

body_estimation = None
model_path = 'openpose_models/body_pose_model.pth'
body_estimation = Body(model_path)