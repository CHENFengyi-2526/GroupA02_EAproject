CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('cb723cc226d7');
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	slug VARCHAR(64) NOT NULL, 
	description TEXT, 
	sort_order INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (slug)
);
INSERT INTO categories VALUES(1,'ASP.NET Core Basics','aspnet-core-basics','Learn the core concepts of ASP.NET Core',10);
INSERT INTO categories VALUES(2,'Getting Started','getting-started','Set up your environment and build your first ASP.NET Core app.',10);
INSERT INTO categories VALUES(3,'Fundamentals	','fundamentals','Core concepts: middleware, dependency injection, configuration.',20);
INSERT INTO categories VALUES(4,'MVC','mvc','Model-View-Controller, Razor views, tag helpers, routing.',30);
INSERT INTO categories VALUES(5,'Web API','web-api','Build RESTful APIs, Swagger documentation, versioning.	',40);
INSERT INTO categories VALUES(6,'Blazor','blazor','Interactive web UI with Blazor Server and WebAssembly.',50);
CREATE TABLE resource_categories (
	id INTEGER NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	slug VARCHAR(64) NOT NULL, 
	icon VARCHAR(50), 
	description TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (slug)
);
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	description VARCHAR(200), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO roles VALUES(1,'admin','administrator');
CREATE TABLE tags (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	slug VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (slug)
);
INSERT INTO tags VALUES(1,'aspnetcore','aspnetcore');
INSERT INTO tags VALUES(2,'tutorial','tutorial');
INSERT INTO tags VALUES(3,'dependency-injection','dependency-injection');
INSERT INTO tags VALUES(4,'ioc','ioc');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(64) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(256) NOT NULL, 
	bio TEXT, 
	avatar VARCHAR(200), 
	created_at DATETIME, 
	last_seen DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO users VALUES(1,'Evie','111@gmail.com','pbkdf2:sha256:600000$VQyrwQUQcQt221wG$6933ff06daa9c03f9941118371686a8a4673f95ed5e5d7cc8965b848faa4a03c',NULL,NULL,'2026-04-04 17:51:27.288491','2026-04-21 15:09:04.698706');
INSERT INTO users VALUES(2,'testuser1','testuser1@gmail.com','pbkdf2:sha256:600000$phQr2oKmcdeL5qTK$fac5dc893679becdbab1722792ccf3f4425c07045ebaafc78bd9c41b4934ade4',NULL,NULL,'2026-04-06 07:50:00.317248','2026-04-06 13:45:35.486076');
INSERT INTO users VALUES(3,'testuser2','testuser2@gmail.com','pbkdf2:sha256:600000$ZKJEy6SXUAV8t2R2$817644a597b57e41ead226c1db74d65b6678c79358bf98bb1796aac4fb12aad1',NULL,NULL,'2026-04-06 10:37:16.738310','2026-04-06 10:37:19.869111');
INSERT INTO users VALUES(4,'testadmin1','testadmin1@example.com','pbkdf2:sha256:600000$Y198O7AuyYg6UUVm$2623e316a6015c4aeb152c0f0f3dddfec8d32c762448931c9a5253a5cfedac4e',NULL,NULL,'2026-04-06 13:23:10.612097','2026-04-21 14:52:14.443098');
CREATE TABLE discussion_posts (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	content TEXT NOT NULL, 
	category VARCHAR(50), 
	view_count INTEGER, 
	reply_count INTEGER, 
	is_pinned BOOLEAN, 
	is_closed BOOLEAN, 
	user_id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, is_edited BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO discussion_posts VALUES(1,'Test','123','general',115,8,0,0,2,'2026-04-06 08:10:01.862272','2026-04-06 13:45:38.454418',NULL);
INSERT INTO discussion_posts VALUES(2,'Admin Test Post','Admin Test Post','general',1,0,0,0,4,'2026-04-06 13:48:20.642998','2026-04-06 13:48:20.659930',NULL);
INSERT INTO discussion_posts VALUES(3,'Admin test pin post 2','Admin test pin post 2','general',1,0,0,0,4,'2026-04-06 13:59:53.699690','2026-04-06 13:59:53.717438',NULL);
INSERT INTO discussion_posts VALUES(4,'Admin test pin post 3','Admin test pin post 3','general',4,0,1,0,4,'2026-04-06 14:03:55.010488','2026-04-18 13:50:34.240430',NULL);
INSERT INTO discussion_posts VALUES(5,'test post 4','test post 4','showcase',2,0,0,0,4,'2026-04-06 14:05:57.890389','2026-04-18 14:17:50.621528',NULL);
INSERT INTO discussion_posts VALUES(6,'test post5','test post5','help',1,0,0,0,4,'2026-04-06 14:06:06.492550','2026-04-06 14:06:06.511112',NULL);
INSERT INTO discussion_posts VALUES(7,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:43:46.500315','2026-04-06 14:43:46.515798',NULL);
INSERT INTO discussion_posts VALUES(8,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:43:50.951830','2026-04-06 14:43:50.965934',NULL);
INSERT INTO discussion_posts VALUES(9,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:43:55.255363','2026-04-06 14:43:55.269848',NULL);
INSERT INTO discussion_posts VALUES(10,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:43:59.006082','2026-04-06 14:43:59.020265',NULL);
INSERT INTO discussion_posts VALUES(11,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:44:03.541236','2026-04-06 14:44:03.554698',NULL);
INSERT INTO discussion_posts VALUES(12,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:44:08.504149','2026-04-06 14:44:08.517019',NULL);
INSERT INTO discussion_posts VALUES(13,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:44:12.552972','2026-04-06 14:44:12.567674',NULL);
INSERT INTO discussion_posts VALUES(14,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:44:19.049893','2026-04-06 14:44:19.064436',NULL);
INSERT INTO discussion_posts VALUES(15,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:44:24.049919','2026-04-06 14:44:24.065339',NULL);
INSERT INTO discussion_posts VALUES(16,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:44:28.287169','2026-04-06 14:44:28.301894',NULL);
INSERT INTO discussion_posts VALUES(17,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:44:31.834588','2026-04-06 14:44:31.847687',NULL);
INSERT INTO discussion_posts VALUES(18,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:47:46.158235','2026-04-06 14:47:46.171689',NULL);
INSERT INTO discussion_posts VALUES(19,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:47:50.316341','2026-04-06 14:47:50.329391',NULL);
INSERT INTO discussion_posts VALUES(20,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:47:53.333590','2026-04-06 14:47:53.348360',NULL);
INSERT INTO discussion_posts VALUES(21,'temp post','temp post','general',1,0,0,0,4,'2026-04-06 14:47:56.107292','2026-04-06 14:47:56.121757',NULL);
INSERT INTO discussion_posts VALUES(22,'temp post','temp post','general',2,0,0,0,4,'2026-04-06 14:47:59.865114','2026-04-18 13:48:44.281912',NULL);
INSERT INTO discussion_posts VALUES(23,'temp post','temp post','general',2,0,0,0,4,'2026-04-06 14:48:02.648902','2026-04-18 13:07:59.846620',NULL);
CREATE TABLE resources (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	description TEXT, 
	type VARCHAR(20) NOT NULL, 
	file_path VARCHAR(500), 
	external_link VARCHAR(500), 
	file_size VARCHAR(50), 
	download_count INTEGER, 
	is_featured BOOLEAN, 
	user_id INTEGER NOT NULL, 
	category_id INTEGER, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES resource_categories (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE tutorials (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	summary TEXT, 
	content TEXT NOT NULL, 
	difficulty VARCHAR(20), 
	estimated_minutes INTEGER, 
	is_published BOOLEAN, 
	view_count INTEGER, 
	like_count INTEGER, 
	user_id INTEGER NOT NULL, 
	category_id INTEGER, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	UNIQUE (slug)
);
INSERT INTO tutorials VALUES(1,'Introduction to ASP.NET Core','intro-to-aspnet-core','Learn what ASP.NET Core is and how to build your first app.','ASP.NET Core','beginner',15,1,4,0,4,1,'2026-04-08 06:07:25.385207','2026-04-21 14:42:09.416133');
INSERT INTO tutorials VALUES(2,'Install .NET SDK and Create Your First Project','install-dotnet-sdk-first-project','Learn how to install the .NET SDK, create a new ASP.NET Core project, and run it.',replace(replace('<p>In this tutorial, you''ll set up your development environment and create your first ASP.NET Core web application.</p>\r\n<h2>Step 1: Install .NET SDK</h2>\r\n<p>Go to <a href="https://dotnet.microsoft.com/download">dotnet.microsoft.com/download</a> and download the latest .NET SDK for your OS.</p>\r\n<h2>Step 2: Create a new project</h2>\r\n<pre><code>dotnet new webapp -n MyFirstApp','\r',char(13)),'\n',char(10)),'beginner',10,0,1,0,4,1,'2026-04-21 14:58:11.522762','2026-04-21 14:58:11.700607');
INSERT INTO tutorials VALUES(3,'Introduction to Dependency Injection in ASP.NET Core','dependency-injection-basics','Learn how to register and use services with built-in DI container.',replace(replace('<p>ASP.NET Core has built-in support for dependency injection. It promotes loose coupling and testability.</p>\r\n<h2>Register a service</h2>\r\n<pre><code>builder.Services.AddScoped&lt;IMyService, MyService&gt;();</code></pre>\r\n<h2>Inject in a controller</h2>\r\n<pre><code>public class HomeController : Controller\r\n\r\n{\r\nprivate readonly IMyService _service;\r\npublic HomeController(IMyService service) => _service = service;\r\n}</code></pre>\r\n\r\n- **Difficulty**: Beginner\r\n- **Est. Minutes**: 10\r\n- **Published**: Yes\r\n- **Tags**: `dependency-injection, ioc`\r\n\r\n---\r\n\r\n## 教程 4：配置入门（appsettings.json）\r\n- **Title**: Configuration in ASP.NET Core\r\n- **Slug**: configuration-appsettings-json\r\n- **Summary**: How to read settings from appsettings.json and environment variables.\r\n- **Content**:\r\n```html\r\n<p>ASP.NET Core uses a flexible configuration system. Start with <code>appsettings.json</code>.</p>\r\n<h2>Example appsettings.json</h2>\r\n<pre><code>{\r\n"Logging": { ... },\r\n"MySetting": "Hello World"\r\n}</code></pre>\r\n<h2>Read in code</h2>\r\n<pre><code>var mySetting = Configuration["MySetting"];</code></pre>','\r',char(13)),'\n',char(10)),'beginner',10,1,1,0,1,1,'2026-04-21 15:31:59.184661','2026-04-21 15:31:59.264677');
CREATE TABLE user_roles (
	user_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id, role_id), 
	FOREIGN KEY(role_id) REFERENCES roles (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO user_roles VALUES(4,1);
CREATE TABLE downloads (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	resource_id INTEGER NOT NULL, 
	downloaded_at DATETIME, 
	ip_address VARCHAR(45), 
	PRIMARY KEY (id), 
	FOREIGN KEY(resource_id) REFERENCES resources (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE post_comments (
	id INTEGER NOT NULL, 
	content TEXT NOT NULL, 
	post_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	parent_id INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES post_comments (id), 
	FOREIGN KEY(post_id) REFERENCES discussion_posts (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO post_comments VALUES(1,'test reply',1,2,NULL,'2026-04-06 08:17:35.522686');
INSERT INTO post_comments VALUES(2,replace(replace('test reply 2\r\n','\r',char(13)),'\n',char(10)),1,2,NULL,'2026-04-06 08:20:51.773214');
INSERT INTO post_comments VALUES(3,'test reply comment',1,2,1,'2026-04-06 10:45:09.019173');
INSERT INTO post_comments VALUES(4,'123',1,2,1,'2026-04-06 10:46:30.375262');
INSERT INTO post_comments VALUES(5,'123',1,2,3,'2026-04-06 10:48:02.145393');
INSERT INTO post_comments VALUES(6,'456',1,2,1,'2026-04-06 10:51:04.474213');
INSERT INTO post_comments VALUES(7,'12345',1,2,2,'2026-04-06 12:13:49.301165');
INSERT INTO post_comments VALUES(8,replace(replace('Test Comment 3\r\n','\r',char(13)),'\n',char(10)),1,2,NULL,'2026-04-06 12:14:02.308709');
CREATE TABLE post_likes (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(post_id) REFERENCES discussion_posts (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	UNIQUE (user_id, post_id)
);
INSERT INTO post_likes VALUES(1,2,1,'2026-04-06 10:36:09.550943');
INSERT INTO post_likes VALUES(2,3,1,'2026-04-06 10:37:32.192349');
CREATE TABLE tutorial_tags (
	tutorial_id INTEGER NOT NULL, 
	tag_id INTEGER NOT NULL, 
	PRIMARY KEY (tutorial_id, tag_id), 
	FOREIGN KEY(tag_id) REFERENCES tags (id), 
	FOREIGN KEY(tutorial_id) REFERENCES tutorials (id)
);
INSERT INTO tutorial_tags VALUES(1,1);
INSERT INTO tutorial_tags VALUES(1,2);
INSERT INTO tutorial_tags VALUES(2,1);
INSERT INTO tutorial_tags VALUES(2,2);
INSERT INTO tutorial_tags VALUES(3,3);
INSERT INTO tutorial_tags VALUES(3,4);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE UNIQUE INDEX ix_users_username ON users (username);
