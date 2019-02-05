#  Tutorial: WRF point extraction

This example shows how to extract a timeseries of temperature values for some locations specified with lat/lon from the [dynamically downscaled climate data for Alaska](https://registry.opendata.aws/wrf-alaska-snap/).  This tutorial assumes you have basic knowledge about how to launch an EC2 instance on AWS, and basic knowledge about using the command line in Linux.

Open the EC2 console, **switch to the US West (Oregon) region**, and choose "Launch instance".  Search for `ami-000c6d1a9c74d8bab` and select that image from the Community results.  Configure the instance if you wish (defaults are fine for this demo) and launch.

Connect to the instance as the `centos` user.

After logging in as the `centos` user, start by cloning this repository:

```
git clone https://github.com/ua-snap/tutorials
cd tutorials/WRF
```

Next, **mount the WRF s3 data bucket**.  We use [s3fs](https://github.com/s3fs-fuse/s3fs-fuse) for this.

```
s3fs -o public_bucket=1,use_cache=/tmp,ro,allow_other,umask=0022 wrf-ak-ar5 ~/wrf-ak-ar5
```

Finally, run the script inside the `pipenv` environment:

```
pipenv run python extract_points_wrf.py
```

After a few minutes, the script should produce a file named `extracted.csv`.

## What next?

 * Modify the script to pull data for a community you are interested in.
