files under either hooks directory MUST BE executables, no text no nothing, everything will be RUN via sh
confighooks only run after config changes but not during deploy
hooks only run after deploy but not after config  changes
there are ALWAYS download from the zip(upload to S3) so local modification is not possible except deploy hook which can be process by .ebextensions
so if the source is from Windows, confighooks will always fail, don't use it
for hooks(deploy), use dos2unix(\r would chok) and chmod to change attributes before running them if they are created in windows
