FROM gradle:8.7-jdk21 AS build

WORKDIR /app

COPY . .

RUN ./gradlew bootWar -x test

FROM eclipse-temurin:21-jre-jammy

WORKDIR /app

FROM tomcat:10.1.24-jre21-temurin-jammy

WORKDIR /usr/local/tomcat/webapps/

RUN rm -rf ROOT && rm -rf examples

COPY --from=build /app/build/libs/*.war ROOT.war

EXPOSE 8080

CMD ["catalina.sh", "run"]

LABEL description="Conteneur de l'application Java"