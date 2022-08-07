import route_from_points
from data_apis import rtm_zones
import numpy as np


def get_path_distances(df):
    # get rtm zones
    zones = rtm_zones.get_rtm_zones()

    # get rtm zones coordinates
    rtm_zones_coords = zones.geometry.centroid.apply(lambda x: (x.y, x.x))

    pts = np.array(rtm_zones_coords)

    ground_dist = np.abs(pts[np.newaxis, :, :] - pts[:, np.newaxis, :]).min(axis=2)
    ride_dist = np.empty_like(ground_dist)
    for i in range(len(pts) - 1):
        for j in range(i + 1, len(pts)):
            dist = route_from_points.route_from_points(df, pts[i], pts[j])
            ride_dist[i, j] = dist
    return ground_dist, ride_dist


if __name__ == '__main__':
    get_path_distances()
