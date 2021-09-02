# jekyll-intel-gamedev

## Setting up with Jekyll for the first time

1. **Install Ruby**
	- It's recommended to use some kind of ruby environment manager. This repo was made using [rbenv](https://github.com/rbenv/rbenv) at ruby 3.0.2. If `rbenv` is installed, the `.ruby-version` file will hint `rbenv` to use this version when in the repo.
2. **Install Bundler:** Run `gem install bundler` into the terminal to install globally.

## Development

To set up your environment to develop this theme, run `bundle install` inside the repo directory.

To test the site, run `bundle exec jekyll serve --livereload --config _config_local.yml` and open your browser at `http://localhost:4000`. You can also add `--livereload` for browser sync. You may need to generate content before testing the site.

### Content Generation and Sync

The content scraper script is located in `/script`. It needs two pieces of information to run:
* An organization repos URL to scrape, in the form of https://api.github.com/orgs/{org}/repos
* A Github Auth token, such as a PAT, in order to increase the amount of API requests we are able to make

After using Python 3.9+ to install dependencies in `requirements.txt`, you can run the script and provide the above variables in two ways:
1. You can run the script from the console by supplying the information as arguments, in the form `python compile_content.py URL PAT`
2. Or you can set the following environment variables and not provide arguments: `GITHUB_CONTENT_SYNC_ORG_REPOS_URL`, `GITHUB_CONTENT_SYNC_PAT`
	* This can be useful for example when using the script in PyCharm. You can set the environemnt variables once within your configuration.

On a successful run, the script will generate `topics.json` and `projects.json`, and write them to the `_data` folder. It will also write the social images pulled from the repo's meta tags to the image assets folder. This is enough to get the site to generate with default content, for example when you need to test locally. These files do not *need* to be tracked, but can be, e.g. to be used as example or test content. The current github workflow will generate content and use it at site generation, so the idea is to **track your content overrides and generate content at build time.** See more below.

## Config and Content Overrides

The theme is generally configured to take user input in YAML and use this user input to override the content provided from JSON.

### Config

For SEO, reference the `jekyll-seo-tag` documentation for config and content options available through this plugin.

Add pages with a title and a relative URL to `navigation.yml` to populate the menu. The site's URL and baseurl will be preprended automatically. For example:
```yaml
- title: Documentation
  url: /documentation
- title: Projects
  url: /projects
- title: Tools and Libraries
  url: /tools-and-libraries
- title: About
  url: /about
```

### Content Overrides 

Here is how to use the content overrides:

* **Topics**
	* The theme will populate the topics filter with the topics in `topics.json`, but only if the topics are also listed in `userTopics.yml`. The recommended way to maintain this whitelist is to convert `topics.json` into a new file `userTopics.yml`, then remove topics as necessary.
* **Projects**
	* Projects will by default pull most of their information from github, but you can override certain details by creating entries in `projectsOverrides.yml`. Do this by creating an object with the key of the name of the repository you want to pass content overrides to, for example:
	```yaml
	ISPCTextureCompressor:
		show: false
		long_description: This is a long description
	```
	* you can add `show` with a boolean value (default is `true`) to hide specific projects.
	* if an `imgAsset` is set, that image will be pulled from the `assets/images/` folder and used
	* a `long_description` can be used to override the description pulled from Github
* **Homepage Featured Projects**
	* Defining projects in an array in `featured.yml` will cause them to be added to the homepage. Similar content overrides are available. Example:
	```yaml
	- repoName: ISPCTextureCompressor
		headline: This is a custom headline. The default currently is 'Featured Projects.'
		long_description: Features can implement a custom long description. If not provided, the layout will pull the repo's short description from github.
	- repoName: AdaptiveSync
		sliderImg: 500.png
	```

## Adding Styles

Style partials should be added to `_sass` with an underscore, like `_styles.scss`. They should then be imported into `assets/css/main.scss`, which is compiled at site build time.

## JS Minification with gulp

JavaScript minification is handled by a gulp script. The gulp processor will concatenate all files in `assets/js/_src/`, then minify the resutling script. To get started:

1. Install gulp globally with `npm install --global gulp-cli`
2. Install the project with `npm install`

After setting up, you can use `gulp` to run the minification task whenever you want to update `script-min.js` that is shipped with the site. You will also need to run `gulp` to test locally.

**Currently this is not conducted automatically when the site is built via Github Actions.** Note also that the files within `.../_src` are *not* copied over to the site upon build, so `script-min.js` must be present. This means any changes to the minified file should be tracked and pushed manually. The gulp system currently exists just as a simple, repeatable way to edit the site's JS.


## License

The theme is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

