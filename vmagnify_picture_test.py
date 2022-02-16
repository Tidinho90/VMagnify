from vmagnify.vmagnify_picture import VMagnifyPicture

# Launch this script in commandline to test the process of an URL

test = VMagnifyPicture()
test.process_url(
    "https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/images/input.png")
