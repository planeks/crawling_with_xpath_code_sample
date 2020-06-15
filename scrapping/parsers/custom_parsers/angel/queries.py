companies_query = '''
query JobSearchResultsX($filterConfigurationInput: FilterConfigurationInput!) {
talent {
    jobSearchResults(filterConfigurationInput: $filterConfigurationInput) {
    rawQuery
    totalStartupCount
    startups {
        edges {
        node {
            ... on StartupSearchResult {
            ...StartupResultSearchResultFragment
            __typename
            }
            ... on PromotedResult {
            promotionId
            promotedStartup {
                ...StartupResultFragment
                __typename
            }
            __typename
            }
            __typename
        }
        __typename
        }
        __typename
    }
    featuredContentTitle
    featuredContentItems {
        ... on JobCollection {
        ...JobCollectionCardFragment
        __typename
        }
        ... on StartupSearchResult {
        ...StartupResultSearchResultFragment
        __typename
        }
        __typename
    }
    __typename
    }
    __typename
}
}

fragment JobCollectionCardFragment on JobCollection {
id
title
slug
heroUrl
description
__typename
}

fragment StartupResultFragment on Startup {
id
...BadgeBarFragment
...StartupHeaderFragment
...StarStartupButtonFragment
highlightedJobListings {
    ...JobListingListFragment
    __typename
}
__typename
}

fragment BadgeBarFragment on Startup {
id
badges {
    id
    name
    label
    tooltip
    avatarUrl
    __typename
}
__typename
}

fragment StartupHeaderFragment on Startup {
id
name
slug
logoUrl
highConcept
companySize
__typename
}

fragment StarStartupButtonFragment on Startup {
id
currentUserHasStarred
__typename
}

fragment JobListingListFragment on JobListing {
id
createdAt
autoPosted
description
jobType
liveStartAt
locationNames
primaryRoleTitle
remote
slug
title
...JobListingCompensationFragment
__typename
}

fragment JobListingCompensationFragment on JobListingBaseInterfaceType {
id
compensation
estimatedSalary
equity
usesEstimatedSalary
__typename
}

fragment StartupResultSearchResultFragment on StartupSearchResult {
id
...BadgeBarSearchResultFragment
...StartupHeaderSearchResultFragment
...StarStartupSearchResultButtonFragment
highlightedJobListings {
    ...JobListingListSearchResultFragment
    __typename
}
__typename
}

fragment BadgeBarSearchResultFragment on StartupSearchResult {
id
badges {
    id
    name
    label
    tooltip
    avatarUrl
    __typename
}
__typename
}

fragment StartupHeaderSearchResultFragment on StartupSearchResult {
id
name
slug
logoUrl
highConcept
companySize
locationTaggings {
    id
    displayName
    __typename
}
__typename
}

fragment StarStartupSearchResultButtonFragment on StartupSearchResult {
id
currentUserHasStarred
__typename
}

fragment JobListingListSearchResultFragment on JobListingSearchResult {
id
createdAt
autoPosted
description
jobType
liveStartAt
locationNames
primaryRoleTitle
remote
slug
title
...JobListingCompensationSearchResultFragment
__typename
}

fragment JobListingCompensationSearchResultFragment on JobListingSearchResult {
id
compensation
estimatedSalary
equity
usesEstimatedSalary
__typename
}
'''

jobs_query = '''
query JobListingModalQuery($id: ID!) {
  jobListing(id: $id) {
    id
    title
    description
    descriptionHtml
    descriptionType
    slug
    ...DetailsPanelFragment
    ...JobListingCompensationFragment
    startup {
      id
      slug
      ...StartupDetailsFragment
      ...StartupHeaderFragment
      ...BadgeBarFragment
      __typename
    }
    __typename
  }
}

fragment DetailsPanelFragment on JobListingBaseInterfaceType {
  id
  ...JobMetadataFragment
  startup {
    id
    __typename
  }
  recruitingContact {
    id
    ...PersonCardFragment
    __typename
  }
  __typename
}

fragment JobMetadataFragment on JobListingBaseInterfaceType {
  id
  jobType
  yearsExperienceMin
  visaSponsorship
  locationNames
  acceptedRemoteLocationNames
  remote
  skills {
    id
    displayName
    slug
    __typename
  }
  ... on JobListing {
    currentUserQualificationReport {
      errors
      __typename
    }
    __typename
  }
  __typename
}

fragment PersonCardFragment on StartupRole {
  id
  user {
    id
    name
    slug
    avatarUrl
    isCurrentUserFollowing
    pathName
    __typename
  }
  hiredViaTalent
  title
  role
  roleDisplayName
  tenureSeconds
  __typename
}

fragment StartupDetailsFragment on Startup {
  id
  productDescription
  mediaUploads(section: "overview") {
    ...MediaUploadFragment
    __typename
  }
  ...OverviewPeopleFragment
  ...OverviewFundingFragment
  ...OverviewCultureFragment
  ...MetadataFragment
  __typename
}

fragment OverviewFundingFragment on Startup {
  id
  slug
  totalRaisedAmount
  startupRounds {
    totalCount
    edges {
      node {
        id
        roundType
        closedAt
        valuation
        __typename
      }
      __typename
    }
    __typename
  }
  pastInvestorRoles {
    totalCount
    __typename
  }
  __typename
}

fragment OverviewPeopleFragment on Startup {
  id
  slug
  currentFounderRoles {
    ...PersonCardFragment
    ...BioFragment
    ...FollowersFragment
    __typename
  }
  pastFounderRoles {
    ...PersonCardFragment
    ...BioFragment
    ...FollowersFragment
    __typename
  }
  currentTeamMemberRoles(first: 3) {
    totalCount
    edges {
      node {
        ...PersonCardFragment
        ...BioFragment
        ...FollowersFragment
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment BioFragment on StartupRole {
  id
  user {
    id
    htmlBio
    __typename
  }
  __typename
}

fragment FollowersFragment on StartupRole {
  id
  user {
    id
    followers(first: 3) {
      totalCount
      edges {
        node {
          id
          name
          slug
          avatarUrl
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment OverviewCultureFragment on Startup {
  id
  name
  slug
  cultureMediaUploads: mediaUploads(section: "culture") {
    ...MediaUploadFragment
    __typename
  }
  perks: culturePerks {
    ...CulturePerkFragment
    __typename
  }
  __typename
}

fragment MediaUploadFragment on StartupMediaUpload {
  id
  imageUrl
  videoUrl
  videoThumbnailUrl
  mime
  section
  order
  __typename
}

fragment CulturePerkFragment on CulturePerk {
  id
  category
  title
  description
  __typename
}

fragment MetadataFragment on Startup {
  id
  name
  companySize
  totalRaisedAmount
  slug
  ...LinksFragment
  marketTaggings {
    id
    name
    slug
    displayName
    __typename
  }
  locationTaggings {
    id
    name
    slug
    displayName
    __typename
  }
  __typename
}

fragment LinksFragment on Startup {
  id
  companyUrl
  twitterUrl
  blogUrl
  facebookUrl
  linkedInUrl
  productHuntUrl
  __typename
}

fragment StartupHeaderFragment on Startup {
  id
  name
  slug
  logoUrl
  highConcept
  companySize
  __typename
}

fragment BadgeBarFragment on Startup {
  id
  badges {
    id
    name
    label
    tooltip
    avatarUrl
    __typename
  }
  __typename
}

fragment JobListingCompensationFragment on JobListingBaseInterfaceType {
  id
  compensation
  estimatedSalary
  equity
  usesEstimatedSalary
  __typename
}
'''