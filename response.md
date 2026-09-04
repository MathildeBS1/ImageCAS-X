Hey Mathilde, 

Great questions! I have had little experience with the Copenhagen General Population Study (Herlev/Østerbro) actually. I am just starting to get more involved in it, so this will be a learning journey for the two of us. 

There is no coronary segmentation ground truth for any of the data yet, but there are plans to use Medis QAngio software to do it soon. However, the software does not always output the intermediate contours, and usually just outputs the plaque volumes which is not that useful for us. There are ongoing efforts by myself and Phillip to get these intermediates. We are making progress and I'll update you if we get anywhere. The Medis Qangio and ImageCAS-X labelling protocols will likely be different and I suspect that using the Medis software they will not annotate all branches. 

The plan was always to label the lumen ImageCAS (done), train lumen segmentation models (done) and then predict on the CGPS scans (todo). We are currently labelling the outer vessel wall in ImageCAS and will use that to train a model which will use to predict on CGPS. In an ideal world, the predictions will be high enough quality that we do not need to make any manual corrections, but that it still to be seen. 

Either way I suggest that we get both you and Danina to use our in-house labelling software to label the coronary centerlines, lumen and plaque in a small subset of CGPS. This will be a good learning experience for you to understand the data, and can be one way that you validate any methods you develop.  

There are repeat scans of the same patient over time. Around 2000 I believe, and that number is increasing. There are also outcome statistics which describe major adverse cardiac events, amongst many other things. Phillip will know and we can ask him during the meeting tomorrow. 

Hope that helps, we can discuss more tomorrow. 