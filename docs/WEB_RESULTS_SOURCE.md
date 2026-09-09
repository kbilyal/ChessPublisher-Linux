# Web result source

Results entered through Web Arbiter Access are pending organizer submissions in the Hub Worker (`cloud_arbiter_results`), not direct mutations of the normal Cloud snapshot. Linux `Download Results` therefore reads the authenticated `/arbiter-results` queue and acknowledges reviewed rows only after local processing.
