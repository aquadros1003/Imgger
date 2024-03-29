import React, { useState, useEffect } from "react";
import FormContainer from "../components/FormContainer";
import { Form, Button, Row, Col } from "react-bootstrap";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../actions/userActions";
import axios from "axios";
import Message from "../components/Message";
import Loader from "../components/Loader";
import { url } from "../constants/host";
import { toast } from "react-hot-toast";

function LoginScreen() {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");

	const dispatch = useDispatch();

	const location = useLocation();
	const navigate = useNavigate();

	const userLogin = useSelector((state) => state.userLogin);
	const { error, loading, userInfo } = userLogin;

	const redirect = location.search ? location.search.split("=")[1] : "/";

	const [isForgot, setIsForgot] = useState(false);
	const [email, setEmail] = useState("");
	const [sendEmailSuccess, setSendEmailSuccess] = useState(false);

	useEffect(() => {
		if (userInfo?.user) {
			navigate(redirect);
			toast.success(`Successfully logged in ${userInfo?.user.username}`, {
				position: "top-center",
				style: {
					fontSize: "25px",
				},
			});
		} else {
			navigate("/login");
		}
	}, [navigate, userInfo, redirect]);

	const submitHandler = (e) => {
		e.preventDefault();
		dispatch(login(username, password));
	};

	const sendEmail = async () => {
		const config = {
			headers: {
				"Content-type": "application/json",
			},
		};

		const { data } = await axios.post(
			`${url}/graphql`,
			{
				query: `
       mutation {
        sendPasswordResetEmail(email: "${email}"){
            success
            errors
        }
      }
	  `,
			},
			config
		);

		if (data?.data?.sendPasswordResetEmail?.success) {
			await setSendEmailSuccess(true);
		}
	};

	return (
		<div>
			{isForgot ? (
				<FormContainer>
					<h1 className="text-5xl text-center mb-5 underline decoration-double decoration-amber-500">
						Reset your password
					</h1>

					{sendEmailSuccess === true && (
						<Message variant="success">
							Password reset email successfully sent, go to your email
						</Message>
					)}

					<Form className="text-2xl">
						<Form.Group controlId="username">
							<Form.Label>
								{" "}
								<i class="fa-solid fa-user-tag"></i> Email
							</Form.Label>
							<Form.Control
								type="text"
								placeholder="Enter your email address"
								onChange={(ele) => setEmail(ele.target.value)}
							></Form.Control>
						</Form.Group>

						<Button
							className="mt-4 button-primary text-2xl "
							onClick={sendEmail}
						>
							Send email
						</Button>
					</Form>

					<Row className="py-3">
						<Col className="text-center text-xl">
							Do you need account?{" "}
							<Link
								to={"/register"}
								className="text-red-700 hover:text-red-800"
							>
								{" "}
								Sign up
							</Link>
						</Col>
					</Row>
				</FormContainer>
			) : (
				<FormContainer>
					<h1 className="text-5xl text-center mb-5 underline decoration-double decoration-amber-500">
						Sign in
					</h1>

					{error && <Message variant="danger">{error}</Message>}
					{loading && <Loader />}

					<Form onSubmit={submitHandler} className="text-2xl">
						<Form.Group controlId="username">
							<Form.Label>
								{" "}
								<i class="fa-solid fa-user-tag"></i> Username or email address
							</Form.Label>
							<Form.Control
								type="text"
								placeholder="Enter your username / email"
								value={username}
								onChange={(e) => setUsername(e.target.value)}
							></Form.Control>
						</Form.Group>

						<Form.Group controlId="password" className="mt-3">
							<Form.Label>
								<i class="fa-solid fa-lock"></i> Password
							</Form.Label>
							<Form.Control
								type="password"
								placeholder="Enter your password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							></Form.Control>
						</Form.Group>

						<Row className="py-3">
							<Col className="text-center text-base">
								Don't remember password?{" "}
								<Link
									onClick={() => setIsForgot(true)}
									className="text-red-700 hover:text-red-800"
								>
									{" "}
									Reset them
								</Link>
							</Col>
						</Row>
						<Button
							type="submit"
							variant="primary"
							className="mt-4 button-primary text-2xl "
						>
							Sign in
						</Button>
					</Form>

					<Row className="py-3">
						<Col className="text-center text-xl">
							Do you need account?{" "}
							<Link
								to={"/register"}
								className="text-red-700 hover:text-red-800"
							>
								{" "}
								Sign up
							</Link>
						</Col>
					</Row>
				</FormContainer>
			)}

			<FormContainer>
				<h1 className="text-base text-center mb-4 underline decoration-double decoration-amber-500">
					Sign in using
				</h1>
				<div className="flex gap-3 justify-center">
					<Form.Group controlId="fb-login">
						<Link to={"/"} className="text-5xl hover:text-blue-500">
							<i class="fa-brands fa-facebook"></i>
						</Link>
					</Form.Group>

					<Form.Group controlId="apple-login">
						<Link to={"/"} className="text-5xl hover:text-stone-500">
							<i class="fa-brands fa-apple"></i>
						</Link>
					</Form.Group>

					<Form.Group controlId="apple-login">
						<Link to={"/"} className="text-5xl hover:text-sky-500">
							<i class="fa-brands fa-square-twitter"></i>
						</Link>
					</Form.Group>
				</div>
			</FormContainer>
		</div>
	);
}

export default LoginScreen;
