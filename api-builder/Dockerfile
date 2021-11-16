FROM golang:1.13
WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY *.go ./

RUN go build -o /api-builder

CMD [ "/api-builder" ]