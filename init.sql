INSERT INTO language (id, label, shortened, is_activate) VALUES
(1, 'French', 'fr', true),
(2, 'English', 'en', true);

INSERT INTO role (id, label, is_activate) VALUES
(1, 'ROLE_USER', true),
(2, 'ROLE_PREMIUM', true),
(3, 'ROLE_ADMIN', true);

INSERT INTO type (id, label, is_activate) VALUES
(1, 'Tourism', true),
(2, 'Roadtrip', true),
(3, 'Backpacking', true);

INSERT INTO level (id, label, is_activate) VALUES
(1, 'Beginner', true),
(2, 'Intermediate', true),
(3, 'Advanced', true);

INSERT INTO interest (id, label, is_activate) VALUES
(1, 'Culture', true),
(2, 'Nature', true),
(3, 'Discover', true),
(4, 'Gastronomy', true),
(5, 'Monument', true);

INSERT INTO aclroute(id, label, is_activate) VALUES
(1, '^.*$', true),
(2, '^\/admin\/.*$', true),
(3, '^\/user\/$', true),
(4, '^\/user\/profile$', true),
(5, '^\/user\/details\/[0-9]*$', true),
(6, '^\/user\/update\/[0-9]*$', true),
(7, '^\/user\/update\/password\/[0-9]*$', true),
(8, '^\/user\/update\/language\/[0-9]*$', true),
(9, '^\/user\/delete\/[0-9]*$', true),
(10, '^\/level\/$', true),
(11, '^\/level\/details\/[0-9]*$', true),
(12, '^\/level\/add$', true),
(13, '^\/level\/update$', true),
(14, '^\/level\/delete\/[0-9]*$', true),
(15, '^\/type\/$', true),
(16, '^\/type\/details\/[0-9]*$', true),
(17, '^\/type\/add$', true),
(18, '^\/type\/update$', true),
(19, '^\/type\/delete\/[0-9]*$', true),
(20, '^\/role\/$', true),
(21, '^\/role\/details\/[0-9]*$', true),
(22, '^\/role\/add$', true),
(23, '^\/role\/update$', true),
(24, '^\/role\/delete\/[0-9]*$', true),
(25, '^\/acl-bundle\/$', true),
(26, '^\/acl-bundle\/details\/[0-9]*$', true),
(27, '^\/acl-bundle\/add$', true),
(28, '^\/acl-bundle\/update$', true),
(29, '^\/acl-bundle\/delete\/[0-9]*$', true),
(30, '^\/acl-route\/$', true),
(31, '^\/acl-route\/details\/[0-9]*$', true),
(32, '^\/acl-route\/add$', true),
(33, '^\/acl-route\/update$', true),
(34, '^\/acl-route\/delete\/[0-9]*$', true),
(35, '^\/interest\/$', true),
(36, '^\/interest\/details\/[0-9]*$', true),
(37, '^\/interest\/add$', true),
(38, '^\/interest\/update$', true),
(39, '^\/interest\/delete\/[0-9]*$', true),
(40, '^\/language\/$', true),
(41, '^\/language\/details\/[0-9]*$', true),
(42, '^\/language\/add$', true),
(43, '^\/language\/update$', true),
(44, '^\/language\/delete\/[0-9]*$', true),
(45, '^\/itinerary\/$', true),
(46, '^\/itinerary\/list$', true),
(47, '^\/itinerary\/details\/[0-9]*$', true),
(48, '^\/itinerary\/update\/title\/[0-9]*$', true),
(49, '^\/itinerary\/update$', true),
(50, '^\/itinerary\/create', true),
(51, '^\/itinerary\/delete\/[0-9]*$', true);

INSERT INTO aclbundle(id, label, is_activate) VALUES
(1, 'USER_BUNDLE', true),
(2, 'PREMIUM_USER_BUNDLE', true),
(3, 'ADMIN_BUNDLE', true);


INSERT INTO aclbundle_aclroute(id, acl_bundle_id, acl_route_id) VALUES
(1, 3, 1),
(2, 1, 3),
(3, 1, 4),
(4, 1, 6),
(6, 1, 7),
(7, 1, 8),
(8, 1, 9),
(9, 1, 10),
(10, 1, 15),
(11, 1, 35),
(12, 1, 40),
(13, 1, 45),
(14, 1, 46),
(15, 1, 47),
(16, 1, 48),
(17, 1, 49),
(18, 1, 50),
(19, 1, 51),
(20, 2, 3),
(21, 2, 4),
(22, 2, 5),
(23, 2, 6),
(24, 2, 7),
(25, 2, 8),
(26, 2, 9),
(27, 2, 10),
(28, 2, 15),
(29, 2, 35),
(30, 2, 40),
(31, 2, 45),
(32, 2, 46),
(33, 2, 47),
(34, 2, 48),
(35, 2, 49),
(36, 2, 50),
(37, 2, 51);

INSERT INTO role_aclbundle(id, role_id, acl_bundle_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);