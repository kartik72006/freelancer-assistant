def display_result(result):

    analysis = result.analysis
    proposal = result.proposal
    pricing = result.pricing
    review = result.review

    print("\n" + "=" * 70)
    print("FREELANCER ASSISTANT")
    print("=" * 70)

    print("\n📊 ANALYSIS")
    print("-" * 70)
    print(f"Skills: {', '.join(analysis['skills'])}")
    print(f"Complexity: {analysis['complexity']}")
    print(f"Budget: {analysis['budget_estimate']}")
    print(f"Timeline: {analysis['timeline_estimate']}")
    print(f"Category: {analysis['category']}")

    print("\n📂 RELEVANT PROJECTS")
    print("-" * 70)

    for project in analysis["retrieved_projects"]["projects"]:
        print(
            f"• {project['title']} "
            f"(Score: {project['score']})"
        )

    print("\n📝 PROPOSAL")
    print("-" * 70)
    print(proposal)

    print("\n💰 PRICING")
    print("-" * 70)
    print(f"Price: {pricing['price']}")
    print(f"Timeline: {pricing['timeline']}")

    print("\n⭐ REVIEW")
    print("-" * 70)

    print(
        f"Score: {review['score']}"
    )

    for feedback in review["feedback"]:

        if isinstance(feedback, dict):

            print(
                f"\n{feedback['criterion']}"
            )

            if "rating" in feedback:
                print(
                    f"Rating: {feedback['rating']}"
                )

            print(
                f"Comment: {feedback['comment']}"
            )

        else:
            print(f"• {feedback}")

    print("\n" + "=" * 70)