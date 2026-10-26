import NXOpen


def main():
    session = NXOpen.Session.GetSession()
    work_part = session.Parts.Work

    lw = session.ListingWindow
    lw.Open()

    lw.WriteLine("=== SKETCH TEST ===")

    for feature in work_part.Features:

        if getattr(feature, "FeatureType", "").upper() != "SKETCH":
            continue

        lw.WriteLine("")
        lw.WriteLine(
            "Feature: {} | Type: {} | Layer: {}".format(
                getattr(feature, "Name", ""),
                getattr(feature, "FeatureType", ""),
                getattr(feature, "Layer", None),
            )
        )

        try:
            entities = feature.GetEntities()

            lw.WriteLine(
                "Entities: {}".format(len(entities))
            )

            for entity in entities:
                lw.WriteLine(
                    "  Type: {} | Name: {} | Layer: {}".format(
                        type(entity).__name__,
                        getattr(entity, "Name", ""),
                        getattr(entity, "Layer", None),
                    )
                )

        except Exception as exc:
            lw.WriteLine(
                "GetEntities failed: {}".format(exc)
            )


if __name__ == "__main__":
    main()