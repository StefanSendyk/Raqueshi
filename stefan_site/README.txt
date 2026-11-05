Online copies of the big videos, for pages opened on other computers (and the Squarespace version).
They are served by jsDelivr, which only accepts files under 20 MB, so they are re-encoded:
  project1.mp4              1280x720, 25 fps (as filmed), original sound copied untouched
  project2.mp4              1280x720, 50 fps (as filmed), original sound copied untouched
  project3.mp4              1416x720, 30 fps (as filmed), original sound copied untouched
  prelim_final_credits.mp4  1280x720, 30 fps (from 60), original sound copied untouched
jsDelivr also limits how much it serves from one commit (about 50 MB), so the pages load project1.mp4 from a
later commit than the other three. If a link stops working, the pages fall back to media_photos_hq/ next to them.
