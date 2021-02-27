
import argparse
import os


def add_calibration_args(parser):

    parser.add_argument('image_path', help='input image path')

    paths = parser.add_argument_group('paths')

    parser.add_argument('--save', default=None, help='save calibration as json default: input/calibration.json')
    parser.add_argument('--name', default='calibration', help='name for this calibration (used to name output files)')
    parser.add_argument('--output_path', default=None, help='specify output path, default (image_path)')

    image_paths = parser.add_argument_group('image paths')

    image_paths.add_argument('--intrinsic_pattern', type=str, default=None, help='use separate images for intrinsic calibration example "{camera}/intrinsic"')
    image_paths.add_argument('--image_pattern', type=str, default=None, help='pattern to find images for explicitly provided cameras example "{camera}/extrinsic"')

    image_paths.add_argument('--cameras', default=None, help="explicit list of cameras (default: find subdirectories with matching images)")
    image_paths.add_argument('--intrinsic_images', type=int, default=50, help='limit images for initial intrinsic calibration (unlimited)')
   

    camera = parser.add_argument_group('camera settings')
    camera.add_argument('--fix_aspect', default=False, action="store_true", help='force cameras to have same focal length')
    camera.add_argument('--allow_skew', default=False, action="store_true", help='allow skew in intrinsic matrix')

    camera.add_argument('--distortion', default="standard", help='lens distortion model (standard|rational|thin_prism|tilted)')
    camera.add_argument('--master', default=None, help='use camera as master when exporting (default use first camera)')

    optimization = parser.add_argument_group('general optimization settings')
    
    optimization.add_argument('--iter', default=3, help="iterations of bundle adjustment/outlier rejection")
    optimization.add_argument('--boards', default=None, help='configuration file (YAML) for calibration boards')
    optimization.add_argument('--loss', default='linear', help='loss function in optimizer (linear|soft_l1|huber|cauchy|arctan)')

    optimization.add_argument('--outlier', default=5.0, help='threshold for outliers (factor of upper quartile of reprojection error)')
    optimization.add_argument('--auto_scale', default=None, help='threshold for auto_scale to reduce outlier influence (factor of upper quartile of reprojection error) - requires non-linear loss')

    enable = parser.add_argument_group('enable/disable optimization')

    enable.add_argument('--fix_intrinsic', default=False, action='store_true', help='fix intrinsics in optimization')
    enable.add_argument('--fix_camera_poses', default=False, action='store_true', help='fix camera pose optimization')
    enable.add_argument('--fix_board_poses', default=False, action='store_true', help='fix relative board positions (rely on initialization)')
    enable.add_argument('--fix_motion', default=False, action='store_true', help='fix motion optimization (rely on initialization)')
    
    enable.add_argument('--optimize_board', default=False, action='store_true', help='optimize non-planarity of board points')
    enable.add_argument('--motion_model', default="static", help='motion model (rolling|static)')
    

    misc = parser.add_argument_group('misc')

    misc.add_argument('--j', default=len(os.sched_getaffinity(0)), type=int, help='concurrent jobs')
    misc.add_argument('--log_level', default='INFO', help='logging level for output to terminal')
    misc.add_argument('--no_cache', default=False, action='store_true', help="don't load detections from cache")
    misc.add_argument('--show', default=False, action="store_true", help='show result after calibration')



def add_boards_args(parser):
    parser.add_argument('boards',  help='configuration file (YAML) for calibration boards')
    parser.add_argument('--detect', default=None,  help='show detections from an image')


def add_show_args(parser):
    parser.add_argument('workspace_file', help='workspace filename to load')


def parse_with(add_args, **kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    add_args(parser)
    return parser.parse_args()

def parse_arguments():

    parser = argparse.ArgumentParser(prog='multical')
    subparsers = parser.add_subparsers(required=True)

    calibrate_parser = subparsers.add_parser('calibrate')
    add_calibration_args(calibrate_parser)

    boards_parser = subparsers.add_parser('check_boards')
    add_boards_args(boards_parser)

    show_parser = subparsers.add_parser('show_result')
    add_show_args(show_parser)

    return parser.parse_args()

