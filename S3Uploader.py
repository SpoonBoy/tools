import os
import boto3
import argparse


def logging(message):

    """Custom logging function."""

    if args.verbosity and message is not None:
        print(message)


def check_dir(directory_path):

    """
    Test if the given directory is really a directory or a file.
    Return a list of files to be uploaded.
    """

    logging("=== Function check_dir ===")

    files = []

    if os.path.isfile(directory_path):
        logging("\t- The resource is a file.")
        files.append(os.path.absos.path(directory_path))

    if os.path.isdir(directory_path):
        logging("\t- The resource is a directory. walking to get the files")
        for root, directories, filenames in os.walk(directory_path):
            for filename in filenames:
                files.append("{}/{}".format(root, filename))

    return files


def list_buckets():

    """ Return a list of bucket names."""

    logging("=== Function list_buckets ===")

    s3 = boto3.resource("s3")
    return [bucket.name for bucket in s3.buckets.all()]


def check_bucket(bucket_name):

    """Test if a bucket exists by checking it's creation date."""

    logging("=== Function check_bucket ===")

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    logging("\t- Accessing bucket named : {}".format(bucket_name))
    try:
        bucket.creation_date
        logging("\t- {} was created {}".format(
            bucket_name,
            bucket.creation_date))
        return bucket
    except:
        logging("\t- Bucket does not exists")
        return get_bucket(None)


def get_bucket(bucket_name):

    """
    If not bucket was provided in args, ask the user with interaction.
    Otherwise, check if it really exists, and returns it.
    """

    logging("=== Function get_bucket ===")

    if bucket_name is not None:
        logging("\t- Provided bucket was : {}".format(bucket_name))
        return check_bucket(bucket_name)
    else:
        print("No bucket was provided, entering interactive mode :")
        buckets = list_buckets()
        for index, bucket in enumerate(buckets):
            print("\t {0} - {1}".format(index, bucket))

        target = raw_input("Choose a bucket (name or number): ")

        if target.isdigit():
            try:
                return check_bucket(buckets[int(target)])
            except IndexError:
                logging("\tThe bucket you specified does not exists")
                quit()
        else:
            return check_bucket(target)


def s3_upload(bucket, files):

    """Upload the list of files to the given bucket."""

    logging("=== Function s3_upload ===")

    for path_to_file in files:
        with open(path_to_file, 'rb') as f:
            logging("\t- Uploading file {}".format(path_to_file))
            bucket.put_object(Key=path_to_file, Body=f)


def main():

    """
    Main method :
    Use boto3 to upload all files within a directory to a choosen bucket.
    """

    files_to_upload = check_dir(args.directory)

    logging("You're about to upload the given list of files :")
    logging(files_to_upload)

    target = get_bucket(args.bucket)
    logging("Uploading files to {}".format(target.name))

    s3_upload(target, files_to_upload)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--verbosity",
        help="""increase output verbosity.
        For the moment, there is only one level of verbosity though :)""",
        action="count"
    )
    parser.add_argument(
        "directory",
        help="os.path to the directory you want to upload.",
        type=str
    )

    parser.add_argument(
        "-b",
        "--bucket",
        help="the name of the bucket you want to upload your files.",
        type=str
    )

    args = parser.parse_args()

    if args.verbosity:
        print("Verbosity set to level {}".format(args.verbosity))

    main()
