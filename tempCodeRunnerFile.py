
            # Detect eyes
            eyes = eye_cascade.detectMultiScale(roi_gray)

            if not len(eyes):
                t = 0